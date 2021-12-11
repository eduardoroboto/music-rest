from marshmallow import ValidationError

from src.database import *
from flask_restx import Namespace, Resource, fields

from src.schema import PlayListSchema

playlist_ns = Namespace("playlist", description="Playlist Object Calls")

playlist_model = playlist_ns.model('PlayList', {
    'id': fields.Integer(required=False, description='Playlist id'),
    'name': fields.String(required=True, description='Playlist name'),
    'user_id': fields.Integer(required=True, description='Playlist User Id'),
    'musics_list': fields.List(fields.Integer(), description='List of ids of musics')
})

playlist_schema = PlayListSchema()


# Listar os dados de todas as músicas de uma determinada playlist
@playlist_ns.route("/")
class PlayListsApi(Resource):
    @playlist_ns.doc('Get All Playlists')
    @playlist_ns.marshal_list_with(playlist_model)
    def get(self):
        return list(db.playlists.values())

    @playlist_ns.marshal_with(playlist_model)
    @playlist_ns.expect(playlist_model)
    def post(self):
        try:
            new_playlist = playlist_schema.load(playlist_ns.payload)
            db.add_new_playlists(new_playlist)
            return playlist_ns.payload, 200
        except TypeError as err:
            return err.__str__(), 400
        except ValidationError as err:
            return err.messages, 400


@playlist_ns.route('/<int:playlist_id>')
@playlist_ns.param('playlist_id', 'Id que identifica a Playlist')
@playlist_ns.response(404, 'PlayList Not Found')
class PlayListApi(Resource):
    @playlist_ns.doc('Get PlayList')
    @playlist_ns.marshal_with(playlist_model)
    def get(self, playlist_id):
        if playlist_id in db.playlists.keys():
            return db.playlists[playlist_id]
        else:
            playlist_ns.abort(404, f"A playlist de id {playlist_id} não existe")

    @playlist_ns.doc('Delete PlayList')
    def delete(self, playlist_id):
        if playlist_id in db.playlists.keys():
            db.remove_playlist(playlist_id)
            return {0: f'Playlist {playlist_id} deleted'}, 200
        else:
            playlist_ns.abort(404, f"Delete Operation Failed: (the PlayList of id {playlist_id} doesn't exist)")

    @playlist_ns.doc('Update PlayList')
    @playlist_ns.response(400, 'Bad JSON')
    @playlist_ns.response(200, 'PlayList Added')
    @playlist_ns.marshal_with(playlist_model)
    @playlist_ns.expect(playlist_model)
    def put(self, playlist_id):
        if playlist_id in db.playlists.keys():
            try:
                new_playlist = playlist_schema.load(playlist_ns.payload)
                db.update_playlist(new_playlist)
                return new_playlist, 200
            except TypeError as err:
                return err.__str__(), 400
            except ValidationError as err:
                return err.messages, 400
        else:
            playlist_ns.abort(404, f"The Put Operation Failed: (the PlayList of id {playlist_id} doesn't exist)")


# Listar os dados de todas as playlists que contêm uma determinada música
@playlist_ns.route('/music/<int:music_id>')
class MusicPlayListApi(Resource):
    @playlist_ns.doc('Get All Playlists with specific music')
    def get(self, music_id):
        playlists = [db.playlists[key] for key in db.playlists.keys() if music_id in db.playlists[key].musics]
        return playlists

# @playlist_ns.route('/<int:playlist_id>/music/<int:music_id>')
# class PlayListMusicApi(Resource):
#     def get(self, music_id):
#         playlists = [db.playlists[key] for key in db.playlists.keys() if music_id in db.playlists[key].musics]
#         return PlayListSchema(many=True).dump(playlists)
