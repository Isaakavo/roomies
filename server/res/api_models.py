from flask import jsonify, make_response, request
from flask_restful import Resource, abort
from models.models import UserModel, AssignedTaskModel, db
from schemas.schemas import UserSchema, TasksSchema, TokenSchema, LoginSchema, ResponseBody, QuerySchema
from . import oauth2
from .utils.utils import checkForAuthentication, errorHandler, getJsonBody
import datetime

user_schema = UserSchema()
task_schema = TasksSchema()
login_schema = LoginSchema()
token_schema = TokenSchema()
response_body = ResponseBody()
query_schema = QuerySchema()

# Route to get users
# We can get all the users
class Users(Resource):
  def get(self, username=''):
    checkForAuthentication(request)
    if username is not None and username != "":
      user = UserModel.query.filter_by(username=username).first()
      errorHandler(user, 404, 'No user with that username')
      resp = getJsonBody(user.id)
      return response_body.dump(resp), 200
    else:
      allUsers = UserModel.query.all()
      return user_schema.dump(allUsers, many = True), 200

  def post(self):
    data = request.get_json()
    args = user_schema.load(data)
    user = UserModel.query.filter_by(username=args['username']).first()
    if not user:
      user = UserModel(username = args['username'], password = args['password'], created=datetime.datetime.now())
      db.session.add(user)
      db.session.commit()
      resp = user_schema.dump(user)
      return  resp, 201
    resp = make_response(jsonify({'error': 'user name already exists', "user": args['username']}), 409)
    return resp

class Tasks(Resource):
  def get(self):
    current_user = checkForAuthentication(request)
    queries = query_schema.load(request.args)
    if queries.get('limit'):
      response = getJsonBody(current_user['userId'], queries['limit'])
      return response_body.dump(response)
    response = getJsonBody(current_user['userId'])
    return response_body.dump(response)

  def post(self):
    current_user = checkForAuthentication(request)
    data = request.get_json()
    args = task_schema.load(data)
    user = UserModel.query.filter_by(id=current_user['userId']).first()
    errorHandler(user, 404, message='No user found')
    task = AssignedTaskModel(user_id=user.id ,task=args['task'], is_completed=args['is_completed'], description=args['description'], created=datetime.datetime.now())
    user.tasks.append(task)
    db.session.add(user)
    db.session.commit()
    resp = make_response(task_schema.dump(task), 201, {'Location': '' })
    return resp

  # Use only to change task and description
  def patch(self):
    current_user = checkForAuthentication(request)
    data = task_schema.load(request.get_json())
    print(current_user['userId'])
    task = AssignedTaskModel.query.filter_by(id=data.get('id'), user_id=current_user['userId']).first()
    print(task)
    errorHandler(task, 403, 'Not allowed to modify this resource')
    task.task = data.get('task')
    task.description = data.get('description')
    task.is_completed = data.get('is_completed')
    db.session.commit()
    return make_response(task_schema.dump(task), 200)

class Login(Resource):
  def post(self):
    args = login_schema.load(request.form)
    user = UserModel.query.filter_by(username = args['username']).first()
    errorHandler(user, 401, 'Username or password incorrect')
    errorHandler(user.verify_password_hash(args['password']), 401, 'Username or password incorrect')
    acces_token = oauth2.create_acces_token(data= {"userId": user.id})
    return {"token": acces_token, "token_type": "bearer"}
