from marshmallow import fields
from ext import ma

class UserSchema(ma.Schema):
  id = fields.Integer(dump_only=True)
  username = fields.String()
  password = fields.String()
  created = fields.DateTime('%d-%m-%Y %H:%M:%S')
  tasks = fields.Nested('TasksSchema', many=True)

class TasksSchema(ma.Schema):
  id = fields.Integer(dump_only = True)
  task = fields.String()
  username = fields.String()
  description = fields.String()
  created = fields.DateTime('%d-%m-%Y %H:%M:%S')
  ended = fields.DateTime('%d-%m-%Y %H:%M:%S')

