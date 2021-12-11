from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from src.database import db
from src.schema import UserSchema

users_ns = Namespace("users", description="Users Object Calls")

users_model = users_ns.model('Users', {
    'id': fields.Integer(required=False, description='User id'),
    'username': fields.String(required=True, description='User name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'playlists': fields.List(fields.Integer(), description='Lists of ids of playlists'),
})

user_schema = UserSchema()


@users_ns.route('/')
class UsersApi(Resource):
    @users_ns.doc('Get All Users')
    @users_ns.marshal_list_with(users_model)
    def get(self):
        return list(db.users.values())  # Listar os dados de todos os usuários do serviço

    @users_ns.doc('Add New User')
    @users_ns.response(400, 'Bad JSON')
    @users_ns.response(200, 'User Added')
    @users_ns.marshal_with(users_model)
    @users_ns.expect(users_model)
    # @users_ns.expect(users_model)
    def post(self):
        try:
            new_user = user_schema.load(users_ns.payload)
            db.add_new_user(new_user)
            return users_ns.payload, 200
        except TypeError as err:
            return err.__str__(), 400
        except ValidationError as err:
            return err.messages, 400


@users_ns.route("/<int:user_id>")
@users_ns.param("user_id", 'Id que Identifica o Usuário')
@users_ns.response(404, 'User not found')
class UserApi(Resource):
    @users_ns.doc('Get User')
    @users_ns.marshal_with(users_model)
    def get(self, user_id):
        if user_id in db.users.keys():
            return db.users[user_id]
        else:
            users_ns.abort(404, f"Get Operation Failed : (The User of id {user_id} doesn't exist)")

    @users_ns.doc('Delete User')
    def delete(self, user_id):
        if user_id in db.users.keys():
            db.remove_user(user_id)
            return {0: f"User id:{user_id} deleted"}, 200
        else:
            users_ns.abort(404, f"Delete Operation Failed : (the User of id {user_id} doesn't exist)")

    @users_ns.doc('Update User')
    @users_ns.response(400, 'Bad JSON')
    @users_ns.response(200, 'User Added')
    @users_ns.marshal_with(users_model)
    @users_ns.expect(users_model)
    def put(self, user_id):
        if user_id in db.users.keys():
            try:
                new_user = user_schema.load(users_ns.payload)
                db.update_user(new_user, user_id)
                return new_user, 200
            except TypeError as err:
                return err.__str__(), 400
            except ValidationError as err:
                return err.messages, 400
        else:
            users_ns.abort(404, f"The Put Operation Failed: (the user of id {user_id} doesn't exist)")

# # Listar os dados de todas as playlists de um determinado usuário
# @users_ns.route("/<int:user_id>/playlists")
# class UsersPLayListApi(Resource):
#     def get(self, user_id):
#         user = db.users[user_id]
#         playlists = [db.playlists[key] for key in user.playlists]
#         return PlayListSchema(many=True).dump(playlists)
