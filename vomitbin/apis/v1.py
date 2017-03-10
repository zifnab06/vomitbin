from flask_restplus import Namespace, Resource, fields, abort
from flask import current_app, request
from datetime import datetime, timedelta

from database import Paste
from utils import new_paste_id

api = Namespace('v1', description="Legacy zifbin API")

paste_in = api.model('Paste', {
    'paste': fields.String(required=True),
    'language': fields.String(required=False),
    'api_key': fields.String(required=False),
    'expiration': fields.Integer(default=60*60*24*30),
    'domain': fields.String(required=False)
    })

paste_out = api.model('Data', {
    'url': fields.String,
    'expires': fields.Integer
    })

@api.route('/paste')
@api.response(200, 'Paste created successfully')
@api.response(403, 'Bad ApiKey')
class NewPaste(Resource):
    @api.expect(paste_in)
    @api.marshal_with(paste_out)
    def post(self):
        data = request.json
        data['time'] = datetime.utcnow()
        data['name'] = new_paste_id(data['paste'])
        expiration = 0
        if 'expiration' in data:
            expiration = data['expiration']
            data['expire'] = datetime.utcnow() + timedelta(seconds=data['expiration'])
            del data['expiration']
        else:
            expiration = 60 * 60 * 24 * 30
            data['expire'] = datetime.utcnow() + timedelta(days=30)


        if 'domain' in data:
            del data['domain']
        if 'api_key' in data:
            del data['api_key']

        paste = Paste(**data)
        paste.save()

        return {'expires': expiration, 'url': 'https://vomitb.in/{}'.format(data['name'])}

@api.route('/paste/<name>')
@api.response(200, "Paste")
@api.response(404, "Not found")
class GetPaste(Resource):
    def get(self, name):
        paste = Paste.get_by_name(name=name)
        if paste:
            return paste.to_dict()
        else:
            abort(404)
