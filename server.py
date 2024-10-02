import flask
import sqlalchemy.exc
from flask import jsonify, request
from flask.views import MethodView
from models import User, Session
from sqlalchemy.exc import IntegrityError
from shema import UpdateUser,  CreateUser
from pydantic import ValidationError


app = flask.Flask("app")

class HttpError(Exception):

    def __init__(self, status_code: int, error_msg: str | dict | list):
        self.status = status_code
        self.error_msg = error_msg

@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    http_response = jsonify({"status": "error", "message": err.error_msg})
    http_response.status = err.status
    return http_response

def validate_json(json_data: dict, schema_cls: type[CreateUser] | type[UpdateUser]):
   try:
       return schema_cls(**json_data).dict(exclude_unset=True)
   except ValidationError as err:
       errors = err.errors()
       for error in errors:
           error.pop("ctx", None)
       raise HttpError(400, errors)

@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response):
    request.session.close()
    return http_response

def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "User est")
    return user


def get_user(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "User not found")
    return user
class UserView(MethodView):

    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(user.json)
    def post(self):
        json_data = validate_json(request.json, CreateUser)
        user = User(**json_data)
        user = add_user(user)
        return jsonify({"id": user.id})



    def patch(self, user_id):
        json_data = validate_json(request.json, UpdateUser)
        user = get_user(user_id)

        for field, value in json_data.items():
            setattr(user, field, value)
        user = add_user(user)
        return user.json

    def delete(self, user_id):
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "delete"})

user_view = UserView.as_view('user')

app.add_url_rule("/user/", view_func=user_view, methods=["POST"])
app.add_url_rule('/user/<int:user_id>/', view_func=user_view, methods=['GET', 'PATCH', 'DELETE'])

app.run()