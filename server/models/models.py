from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

user_tasks = db.Table(
  "user_tasks",
  db.Column('id', db.Integer, primary_key=True),
  db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('tasks_id', db.Integer, db.ForeignKey('tasks.id')),
)

class UserModel(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(25), unique= True,nullable = False)
  password_hash =  db.Column(db.String(128), nullable = False)
  created = db.Column(db.DateTime, nullable = False)
  tasks = db.relationship('AssignedTaskModel', secondary= user_tasks, backref = 'user_task')

  @property
  def password(self): 
    raise AttributeError('Password is not a readable attrubute')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password_hash(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
      return f'UserModel(username={self.username}, password={self.password_hash} ,created={self.created})'

class AssignedTaskModel(db.Model):
  __tablename__ = 'tasks'
  id = db.Column(db.Integer, primary_key = True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  task = db.Column(db.String(50), nullable = False)
  description = db.Column(db.String(200), nullable = True)
  created = db.Column(db.DateTime, nullable = False)
  ended = db.Column(db.DateTime, nullable = True)
  is_completed = db.Column(db.Boolean, nullable = False)
  user = db.relationship('UserModel', secondary=user_tasks, backref='task')

  def __repr__(self):
      return f'AssignedTaskModel(task={self.task}, description={self.description}, created={self.created}, ended={self.ended})'


class ResponseBodyModel():
  def __init__(self, count, tasks) -> None:
      self.count = count
      self.tasks = tasks