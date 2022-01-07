from flask import jsonify, make_response, request, Response
from flask_restful import Resource, abort
from models.models import UserModel, AssignedTaskModel, ResponseBodyModel, db
from schemas.schemas import UserSchema, TasksSchema, TokenSchema, LoginSchema, ResponseBody, QuerySchema
from . import oauth2
import datetime

user_schema = UserSchema()
task_schema = TasksSchema()
login_schema = LoginSchema()
token_schema = TokenSchema()
response_body = ResponseBody()
query_schema = QuerySchema()

class Users(Resource):
  def get(self, username=''):
    authorizationHeader = request.headers.get('Authorization')
    current_user = checkForToken(authorizationHeader)
    if isinstance(current_user, Response):
      return current_user
    if username is not None and username != "":
      user = UserModel.query.filter_by(username=username).first()
      if not user:
        abort(404, message='No user with that username')
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
    authorizationHeader = request.headers.get('Authorization')
    current_user = checkForToken(authorizationHeader)
    if isinstance(current_user, Response):
      return abort(current_user)
    queries = query_schema.load(request.args)
    if queries.get('limit'):
      response = getJsonBody(current_user['userId'], queries['limit'])
      return response_body.dump(response)
    response = getJsonBody(current_user['userId'])
    return response_body.dump(response)

  def post(self):
    authorizationHeader = request.headers.get('Authorization')
    current_user = checkForToken(authorizationHeader)
    if isinstance(current_user, Response):
      return current_user
    data = request.get_json()
    args = task_schema.load(data)
    user = UserModel.query.filter_by(id=current_user['userId']).first()
    if not user:
      abort(404, message='No user found')
    task = AssignedTaskModel(user_id=user.id ,task=args['task'], is_completed=args['is_completed'], description=args['description'], created=datetime.datetime.now(), ended=datetime.datetime.now())
    user.tasks.append(task)
    db.session.add(user)
    db.session.commit()
    # resp = user_schema.dump(user)
    resp = make_response(task_schema.dump(task), 201, {'Location': '' })
    return resp

class Login(Resource):
  def post(self):
    args = login_schema.load(request.form)
    user = UserModel.query.filter_by(username = args['username']).first()
    if not user:
      abort(401, message='Username or password incorrect')
    if not user.verify_password_hash(args['password']):
      abort(401, message='Username or password incorrect')
    acces_token = oauth2.create_acces_token(data= {"userId": user.id})
    return {"token": acces_token, "token_type": "bearer"}

def checkForToken(header):
  if header != None and header != "":
    return oauth2.get_current_user(header)
  else:
    return make_response(jsonify({'error': 'Authorization header missing'}), 403)

def getJsonBody(userId, limit=0):
  if limit != 0:
    tasks = AssignedTaskModel.query.filter_by(user_id=userId).limit(limit).all()
    print(len(tasks))
    return ResponseBodyModel(len(tasks), tasks)
  tasks = AssignedTaskModel.query.filter_by(user_id=userId).all()
  count = AssignedTaskModel.query.filter_by(user_id=userId).count()
  return ResponseBodyModel(count, tasks)