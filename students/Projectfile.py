from flask import Flask,render_template,url_for,flash,redirect,request,session
from students.forms import UploadFileForm,RegistrationForm,LoginForm,ReplyFileForm
from students import app,db,bcrypt
import os
from students.models import User,Abstracts,Upload,Reply
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from flask_login import login_user,current_user,logout_user,login_required


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///details.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
"""
class details(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    TeamName=db.Column(db.String)
    ProjectTitle=db.Column(db.String)
    Department=db.Column(db.String)
    Download=db.Column(db.String)
    Status=db.Column(db.String)
    GuideName=db.Column(db.String)

def __init__(self,TeamName,ProjectTitle,Department,Download,Status,GuideName):
    self.TeamName=TeamName
    self.ProjectTitle=ProjectTitle
    self.Department=Department
    self.Download=Download
    self.Status=Status
    self.GuideName=GuideName
"""

@app.route("/")
@app.route("/home",methods=['GET','POST'])
def home():
    return render_template('home.html')



@app.route("/home/data")
def data():
    return render_template('data.html')



@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/teamregister", methods=['GET', 'POST'])
def teamregister():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('teamregister.html', title='Register', form=form)



@app.route("/home/studentlogin", methods=['GET', 'POST'])
def studentlogin():
    if current_user.is_authenticated:
        return redirect(url_for('student'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(teamname=form.teamname.data).first()
        if user and user.password==form.password.data:
            login_user(user,remember=form.remember.data)
            return redirect(url_for('student'))
        else:
            flash('Login Unsuccessful. Please check teamname and password', 'danger') 
            return redirect(url_for('teamregister'))
    return render_template('studentlogin.html',form=form)


@app.route("/home/guidelogin", methods=['GET', 'POST'])
def guidelogin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('register'))
    return render_template('guidelogin.html', title='Login', form=form)


@app.route("/home/hodlogin", methods=['GET', 'POST'])
def hodlogin():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('register'))
    return render_template('hodlogin.html', title='Login', form=form)




headings=("Team Name","Project Title","Department","Status","View file","Action")
@app.route("/home/guidepage", methods=['GET', 'POST'])
def guidepage():
    if request.method == 'POST':
        if request.form.get('submit1') == 'View Project details':
            return render_template('project_details.html')
        elif  request.form.get('submit2') == 'View Project Status':
            return render_template('project_status.html',headings=headings)
        
    elif request.method == 'GET':
        return render_template('guidepage.html')
    
    return render_template("guidepage.html")





@app.route("/home/Hodpage", methods=['GET', 'POST'])
def Hodpage():
    if request.method == 'POST':
    
            if request.form.get('submit1') == 'View Project details':
                return render_template('project_details1.html',details = details.query.all())
            elif  request.form.get('submit2') == 'View Project Status':
                return render_template('project_status1.html',headings=headings)
        
    elif request.method == 'GET':
        return render_template('Hodpage.html')
    
    return render_template("Hodpage.html")

@app.route("/home/project_status1/reply_by_hod")
def reply_by_hod():
    return render_template('reply_by_hod.html')



@app.route("/home/project_status/reply_by_guide")
def reply_by_guide():
    return render_template('reply_by_guide.html')

@app.route("/home/Hodpage")
def back_hod():
    return render_template('Hodpage.html')

@app.route("/home/guidepage",methods=['GET','POST'])
def back_guide():
    return render_template('guidepage.html')

@app.route("/home/guidepage/project_status",methods=['GET','POST'])
def back_guide1():
    return render_template('project_status.html')

@app.route("/home/Hodpage/project_status1",methods=['GET','POST'])
def back_hod1():
    return render_template('project_status1.html')

@app.route("/home/data/project_details1",methods=['GET','POST'])
def Hodprodet():
    if request.method == 'POST':
        if not request.form['Teamname'] or not request.form['ProjectTitle'] or not request.form['Department'] or not request.form['Download'] or not request.form['Status'] or not request.form['GuideName']:
         flash('Please enter all the fields', 'error')
        else:
            detail = details(request.form['Teamname'], request.form['ProjectTitle'],
            request.form['Department'], request.form['Download'],request.form['Status'],request.form['GuideName'])
            db.session.add(detail)
            db.session.commit()
            return redirect(url_for('project_details1'))
    return render_template('data.html',details = details.query.all())


@app.route("/home/studentlogin/student/upg", methods=['GET',"POST"])
def  upg():
    form = UploadFileForm()
    if form.validate_on_submit():
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                flash("File format not supported.Upload .pdf or .docx")
            else:
                uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        
    return render_template('upg.html',form=form)

@app.route("/home/studentlogin/student/uph")
def  uph():

    return render_template('uph.html')

@app.route("/home/studentlogin/student/vrg")
def  vrg():
    return render_template('vrg.html')

@app.route("/home/studentlogin/student/vrh")
def  vrh():
    return render_template('vrh.html')

@app.route("/home/studentlogin/student", methods=['GET', 'POST'])
def student():
    if request.method == 'GET':
        return render_template('student.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'Upload Project details to Guide':
             redirect(url_for('upg.html'))

        elif  request.form['submit'] == 'Upload Project details to HOD':
             print("hello2")
             return render_template('uph.html')
        elif  request.form['submit'] == 'View reply from Guide':
            return render_template('vrg.html')
        elif  request.form['submit'] == 'View reply from HOD':
            return render_template('vrh.html')
       
        return render_template('student.html')

if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()