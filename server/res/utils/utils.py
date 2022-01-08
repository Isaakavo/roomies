from flask import  jsonify, make_response, Response
from flask_restful import abort
from res import oauth2
from models.models import AssignedTaskModel, ResponseBodyModel

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

def checkForAuthentication(request):
  authorizationHeader = request.headers.get('Authorization')
  current_user = checkForToken(authorizationHeader)
  if isinstance(current_user, Response):
    return abort(current_user)
  return current_user