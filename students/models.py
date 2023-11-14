from enum import unique
from students import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return  User.query.get(user_id)

@login_manager.user_loader
def load_guide(user_id):
    return Userguide.query.get(int(user_id))


@login_manager.user_loader
def load_hod(user_id):
    return Userhod.query.get(int(user_id))


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

class User(db.Model,UserMixin):
    __tablename__ = "user"
    id=db.Column(db.Integer,primary_key=True)
    teamname = db.Column(db.String(20),unique=True)
    guidename = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    abstracts = db.relationship('Abstracts', backref='ab', lazy=True)
    def __repr__(self):
        return f"User('{self.teamname}', '{self.guidename}')"



class Abstracts(db.Model,UserMixin):
     __tablename__ = "abs"
    
     id=db.Column(db.Integer,primary_key=True)
     teamname=db.Column(db.String(20), nullable=False)
     guidename = db.Column(db.String(20), nullable=False)
     title = db.Column(db.String(100) ,nullable=False)
     technology= db.Column(db.String(20), nullable=False)
     filename = db.Column(db.String(100),nullable=False)
     data = db.Column(db.LargeBinary)
     #teamname=db.Column(db.String(20),db.ForeignKey('user.teamname'))
     ab_id=db.Column(db.Integer,db.ForeignKey('user.teamname'))

     '''def __repr__(self):
        return f"Post('{self.teamname}','{self.title}','{self.technology}','{self.filename}')"'''


class Final(db.Model,UserMixin):
     __tablename__ = "final"
     id = db.Column(db.Integer,primary_key=True)
     teamname=db.Column(db.String(20))
     guidename = db.Column(db.String(20), nullable=False)
     title = db.Column(db.String(100) ,nullable=False)
     technology= db.Column(db.String(20), nullable=False)
     filename = db.Column(db.String(100),nullable=False)
     data = db.Column(db.LargeBinary)
     #teamname=db.Column(db.String(20),db.ForeignKey('user.teamname'))
     ab_id=db.Column(db.Integer,db.ForeignKey('user.teamname'))


class Userguide(db.Model,UserMixin):
    __tablename__ = "userguide"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #abstracts=db.relationship('Abstracts',backref='User',lazy=True)
    #abs=db.relationship('Abstracts',backref='user')
        #primaryjoin="User.id==Abstracts.user.id")
    #abstracts = db.relationship('Abstracts', backref='author', lazy=True)
    def __repr__(self):
        return f"Userguide('{self.username}', '{self.email}')"


class Userhod(db.Model,UserMixin):
    __tablename__ = "userhod"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #abstracts=db.relationship('Abstracts',backref='User',lazy=True)
    #abs=db.relationship('Abstracts',backref='user')
        #primaryjoin="User.id==Abstracts.user.id")
    #abstracts = db.relationship('Abstracts', backref='author', lazy=True)
    def __repr__(self):
        return f"Userhod('{self.username}', '{self.email}')"





class Abstractshod(db.Model,UserMixin):
     __tablename__ = "absh"
     id = db.Column(db.Integer, primary_key=True)
     teamname = db.Column(db.String(20),  nullable=False)
     hodname = db.Column(db.String(20), nullable=False)
     guidename = db.Column(db.String(20), nullable=False)
     title = db.Column(db.String(100), nullable=False)
     technology= db.Column(db.String(20), nullable=False)
     filename = db.Column(db.String(100))
     #status=db.Column(db.String(30))
     data = db.Column(db.LargeBinary)
     #user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
     #users=db.Column(db.Integer,db.ForeignKey('user.id'))
     
     def __repr__(self):
        return f"Abstractshod('{self.teamname}','{self.title}','{self.technology}','{self.filename}')"


class Reply(db.Model,UserMixin):
    __tablename__="reply"
    id=db.Column(db.Integer,primary_key=True)
    teamname=db.Column(db.String(100))
    title=db.Column(db.String(100))
    filename=db.Column(db.String(100))
    reply=db.Column(db.String(1000))
    status=db.Column(db.String(1000),default="Pending")

    def __repr__(self):
            return f"reply('{self.teamname}','{self.title}','{self.reply}','{self.status}',{self.filename},'{self.reply}')"


class Replyhod(db.Model,UserMixin):
    __tablename__="replyhod"
    id=db.Column(db.Integer,primary_key=True)
    teamname=db.Column(db.String(100))
    title=db.Column(db.String(100))
    filename=db.Column(db.String(100))
    reply=db.Column(db.String(1000))
    status=db.Column(db.String(1000),default="Pending")

    def __repr__(self):
            return f"reply('{self.teamname}','{self.title}','{self.reply}','{self.status}',{self.filename},'{self.reply}')"
   



   
        