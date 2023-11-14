from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,FileField,EmailField,RadioField
from wtforms.validators import DataRequired,Length,Email,EqualTo,InputRequired,ValidationError
from students.models import User,Reply,Userguide,Upload,Abstracts,Reply,Userhod,Abstractshod,Replyhod
from flask_login import current_user
from wtforms.widgets import TextArea


class ProjectForm1(FlaskForm):
    submit1=SubmitField('Upload Project details to Guide')

class ProjectForm2(FlaskForm):
     submit2=SubmitField('Upload Project details to HOD')

class ProjectForm3(FlaskForm):
    submit3=SubmitField('View reply from Guide')

class ProjectForm4(FlaskForm):
    submit4=SubmitField('View reply from HOD')
    
class UploadFileForm(FlaskForm):
    teamname=StringField('Teamname',validators=[DataRequired()])
    guidename=StringField('Guidename',validators=[DataRequired(),Length(min=2,max=100)])
    project=StringField('Project',validators=[DataRequired(),Length(min=2,max=100)])
    domain=StringField('Technology',validators=[DataRequired(),Length(min=2,max=100)])
    file = FileField("Choose File", validators=[InputRequired()])
    submit=SubmitField("Submit")


class UploadFileFormhod(FlaskForm):
    teamname=StringField('Teamname',validators=[DataRequired()])
    hodname=StringField('Hodname',validators=[DataRequired(),Length(min=2,max=100)])
    guidename=StringField('Guidename',validators=[DataRequired(),Length(min=2,max=100)])
    project=StringField('Project',validators=[DataRequired(),Length(min=2,max=100)])
    domain=StringField('Technology',validators=[DataRequired(),Length(min=2,max=100)])
    file = FileField("Choose File", validators=[InputRequired()])
    submit=SubmitField("Submit")


class RegistrationForm(FlaskForm):
    teamname=StringField('Teamname',validators=[DataRequired(),Length(min=2,max=20)])
    guidename=StringField('Guidename',validators=[DataRequired(),Length(min=2,max=20)])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_teamname(self, teamname):
        user = User.query.filter_by(teamname=teamname.data).first()
        if user:
            raise ValidationError('That teamname is taken. Please choose a different one.')
    
class guideRegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email=EmailField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self, username):
        userguide = Userguide.query.filter_by(username=username.data).first()
        if userguide:
            raise ValidationError('That Username is taken. Please choose a different one.')
   
class hodRegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=100)])
    email=EmailField('Email',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self, username):
        userhod = Userhod.query.filter_by(username=username.data).first()
        if userhod:
            raise ValidationError('That Username is taken. Please choose a different one.')
class LoginForm(FlaskForm):
    teamname=StringField('Teamname',validators=[DataRequired(),Length(min=2,max=100)])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')

class guideloginform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=100)])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')

    
class hodloginform(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=100)])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('remember me')
    submit=SubmitField('Login')


class ReplyFileForm(FlaskForm):
    reply=StringField('Suggestions',validators=[DataRequired(),Length(min=2,max=1000)],widget=TextArea())
    status =RadioField('Status', choices = [('A','Approve'),('R','Reject')])  
    submit=SubmitField('Submit')