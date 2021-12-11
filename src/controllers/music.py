from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError

from ..database import db
from ..schema import MusicSchema

musics_ns = Namespace("musics", description="Music Object Calls")

music_model = musics_ns.model('Music', {
    'id': fields.Integer,
    'artist': fields.String,
    'album': fields.String,
    'name': fields.String,
    'tags': fields.List(fields.String)

})

music_schema = MusicSchema()


# Listar os dados de todas as músicas mantidas pelo serviço
@musics_ns.route("/")
class MusicsApi(Resource):
    @musics_ns.doc('Get All Songs')
    @musics_ns.marshal_list_with(music_model)
    def get(self):
        return list(db.musics.values())

    @musics_ns.doc('Add New Music')
    @musics_ns.response(400, 'Bad JSON')
    @musics_ns.response(200, 'Music Added')
    @musics_ns.marshal_with(music_model)
    @musics_ns.expect(music_model)
    def post(self):
        try:
            new_music = music_schema.load(musics_ns.payload)
            db.add_new_music(new_music)
            return musics_ns.payload, 200
        except TypeError as err:
            return err.__str__(), 400
        except ValidationError as err:
            return err.messages, 400


@musics_ns.route("/<int:music_id>")
@musics_ns.param('music_id', 'Id que identifica a Musica')
@musics_ns.response(200, 'Music Found')
@musics_ns.response(404, 'Music Not Found')
class MusicApi(Resource):
    @musics_ns.doc("Get Music")
    @musics_ns.marshal_with(music_model)
    def get(self, music_id):
        if music_id in db.musics.keys():
            return db.musics[music_id]
        else:
            musics_ns.abort(404, f"The Music of id {music_id} doesn't exist")

    @musics_ns.doc("Delete Music")
    @musics_ns.response(204, 'Music deleted')
    @musics_ns.response(404, 'Music not found')
    def delete(self, music_id):
        if music_id in db.musics.keys():
            db.remove_music(music_id)
            return '', 204
        else:
            musics_ns.abort(404, f"Delete Operation Failed: (the Music of id {music_id} doesn't exist)")

    @musics_ns.doc('Update Songs')
    @musics_ns.marshal_with(music_model)
    @musics_ns.expect(music_model)
    def put(self, music_id):
        if music_id in db.musics.keys():
            try:
                new_music = music_schema.load(musics_ns.payload)
                db.update_music(new_music, music_id)
                return new_music, 200
            except TypeError as err:
                return err.__str__(), 400
            except ValidationError as err:
                return err.messages, 400
        else:
            musics_ns.abort(404, f"The Put Operation Failed: (the music of id {music_id} doesn't exist)")
