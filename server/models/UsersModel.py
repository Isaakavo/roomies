from sharedDb import db

class UserModel(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(25), unique = True, nullable = False)
  password =  db.Column(db.String(15), nullable = False)
  lastLogin = db.Column(db.DateTime, nullable = False)

  def __repr__(self):
      return f'UserModel(username={self.username}, password={self.password}, lastLogin={self.lastLogin}'