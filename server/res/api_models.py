from flask import jsonify, make_response, request, Response
from flask_restful import Resource, abort
from models.models import UserModel, AssignedTaskModel ,db
from schemas.schemas import UserSchema, TasksSchema, TokenSchema, LoginSchema
from . import oauth2
import datetime

user_schema = UserSchema()
task_schema = TasksSchema()
login_schema = LoginSchema()
token_schema = TokenSchema()

class Users(Resource):
  def get(self, username):
    authorizationHeader = request.headers.get('Authorization')
    print(request.headers.get('Authorization'))
    current_user = checkForToken(authorizationHeader)
    if isinstance(current_user, Response):
      return current_user
    if username is not None:
      user = UserModel.query.filter_by(username=username).first()
      return make_response(user_schema.dump(user), 200)
    data = request.get_json()
    username_req = user_schema.load(data)
    user = UserModel.query.filter_by(username=username_req['username']).first()
    if not user:
      print('aborting')
      abort(404, message='No user with that username')
    resp = user_schema.dump(user)
    return resp, 200

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
    # data = [request.headers.get('Authorization'), request.headers.get('tokenType')]
    authorizationHeader = request.headers.get('Authorization')
    current_user = checkForToken(authorizationHeader)
    if isinstance(current_user, Response):
      return current_user
    user = UserModel.query.filter_by(id=current_user['userId']).first()
    return task_schema.dump(user.tasks, many = True)
    # if header != "" and header != None:
    #   decryptToken = oauth2.get_current_user(header)
    #   if isinstance(decryptToken, Response):
    #     return decryptToken 
    #   user = UserModel.query.filter_by(id=decryptToken['userId']).first()
    #   resp = task_schema.dump(user.tasks, many= True)
    #   return resp
    # return 500

  def post(self):
    authorizationHeader = request.headers.get('Authorization')
    # if header == "" or header is None:
    #   return make_response('Missing JWT', 403)
    # current_user = oauth2.get_current_user(header)
    current_user = checkForToken(authorizationHeader)
    if isinstance(current_user, Response):
      return current_user
    data = request.get_json()
    args = task_schema.load(data)
    user = UserModel.query.filter_by(id=current_user['userId']).first()
    if not user:
      abort(404, message='No user found')
    task = AssignedTaskModel(user_id=user.id ,task=args['task'], description=args['description'], created=datetime.datetime.now(), ended=datetime.datetime.now())
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
      abort(404, detail='Invalid Credentials')
    if not user.verify_password_hash(args['password']):
      abort(404, detail='Invalid Credentials')
    #Create a token
    #return token
    acces_token = oauth2.create_acces_token(data= {"userId": user.id})
    return {"acces_token": acces_token, "token_type": "bearer"}



def checkForToken(header):
  if header != None and header != "":
    return oauth2.get_current_user(header)
  else:
    return make_response(jsonify({'error': 'Authorization header missing'}), 403)