from flask import Flask
from flask_restplus import Api, Resource, fields
from domain.model import PhoneCallStart
import infrasctructure.repository as repository
from dateutil import parser
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)
api = Api(app, version='0.1', title='Phone call registry api',
          description='Track down phone calls and coomputes billing data')

ns = api.namespace('phone_calls', description='restfull endpoints')

api_call_start = api.model('CallStart', {
    'start_timestamp': fields.DateTime(),
    'call_id': fields.Integer(),
    'source': fields.String(),
    'destination': fields.String()
})

api_call_end = api.model('CallEnd', {
    'end_timestamp': fields.DateTime(),
    'call_id': fields.Integer(),
})

api_billing = api.model('Billing', {
    'call_destination': fields.String(attribute='destination'),
    'call_date': fields.DateTime(attribute='start_timestamp'),
    'call_duration': fields.String(attribute='call_duration'),
    'call_price': fields.Float(attribute='cost')
})


@ns.route('/call_start')
class PhoneCallStartApi(Resource):
    """phone calls start registry"""
    @ns.doc(model=api_call_start)
    @ns.marshal_with(api_call_start)
    @ns.expect(api_call_start)
    def post(self):
        """Register a phone call start"""
        data = api.payload

        try:
            phone_call = PhoneCallStart(
                parser.parse(data["start_timestamp"]),
                data["call_id"],
                data["source"],
                data["destination"]
            )
        except AssertionError as error:
            return error.args, 400

        repository.session.add(phone_call)
        repository.session.commit()

        return phone_call, 201


@ns.route('/call_end')
class PhoneCallEndApi(Resource):
    """phone calls end registry"""
    @ns.doc('register_phone_call_end')
    @ns.marshal_with(api_call_end)
    @ns.expect(api_call_end)
    def post(self):
        """Register a phone call end"""
        data = api.payload

        try:
            phone_call_start = repository.find_start_call_by_call_id(data["call_id"])
        except NoResultFound:
            return 'no call found by specified call id', 404

        phone_call_start.end_timestamp = parser.parse(data["end_timestamp"]).replace(tzinfo=None)

        # repository.session.add(phone_call_start)
        repository.session.commit()

        return phone_call_start


@ns.route('/billing/<int:year>/<int:month>/<string:number>')
class PhoneBillApi(Resource):
    """phone bills"""
    @ns.doc('phone_bill')
    @ns.marshal_list_with(api_billing)
    def get(self, year: int, month: int, number: str):
        """Show all phone calls with costs within month"""
        phone_calls = repository.find_start_calls_by_phone_number_within_month(year, month, number)
        return phone_calls


if __name__ == '__main__':
    app.run(debug=True)