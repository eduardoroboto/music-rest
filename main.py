from flask import Flask
from flask_restx import Api
from src.controllers.user import users_ns as ns1
from src.controllers.music import musics_ns as ns2
from src.controllers.playlist import playlist_ns as ns3

app = Flask(__name__)
api = Api(
    title="Music Rest",
    version='1.0',
    description='A Music Rest API'
    )

api.init_app(app)


api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)

if __name__ == '__main__':
    app.run(debug=True)
