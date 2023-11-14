from flask import Flask,render_template,url_for,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy
from students.forms import UploadFileForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
app=Flask(__name__)
app.config['UPLOAD_PATH'] = 'static/uploads'
app.config['UPLOAD_EXTENSIONS'] = ['.pdf','.docx']
app.config['SECRET_KEY']='07e6a30e837164493acafb244fcb7989'
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/guide")
def guide():
    return render_template('guide.html')

@app.route("/hod")
def  hod():
    return render_template('hod.html')

@app.route("/upg", methods=['GET',"POST"])
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



@app.route("/uph")
def  uph():

    return render_template('uph.html')

@app.route("/vrg")
def  vrg():
    return render_template('vrg.html')

@app.route("/vrh")
def  vrh():
    return render_template('vrh.html')

@app.route("/student", methods=['GET', 'POST'])
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
    

if __name__=='__main__':
    app.run(debug=True)