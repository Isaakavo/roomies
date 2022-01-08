from marshmallow import fields
from ext import ma

class UserSchema(ma.Schema):
  id = fields.Integer(dump_only=True)
  username = fields.String()
  password = fields.String()
  created = fields.DateTime('%d-%m-%Y %H:%M:%S')
  # tasks = fields.Nested('TasksSchema', many=True)

class TasksSchema(ma.Schema):
  id = fields.Integer()
  task = fields.String()
  is_completed = fields.Boolean()
  # username = fields.String()
  description = fields.String()
  created = fields.DateTime('%d-%m-%Y %H:%M:%S')
  ended = fields.DateTime('%d-%m-%Y %H:%M:%S')
  # access_token = fields.String()

class ResponseBody(ma.Schema):
  count = fields.Integer()
  tasks = fields.Nested(TasksSchema, many=True)
class LoginSchema(ma.Schema):
  username = fields.String()
  password = fields.String()

class TokenSchema(ma.Schema):
  access_token = fields.String()
  # token_type = fields.String()

class TokenDataSchema(ma.Schema):
  userId = fields.Integer()
  exp = fields.Integer()

class QuerySchema(ma.Schema):
  limit = fields.Integer()