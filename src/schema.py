from marshmallow import Schema, fields


class MusicSchema(Schema):
    id = fields.Int()
    artist = fields.Str()
    album = fields.Str()
    name = fields.Str()
    tags = fields.List(fields.Str())


class PlayListSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    user_id = fields.Int()
    musics = fields.List(fields.Int())


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str()
    playlists = fields.List(fields.Int())
