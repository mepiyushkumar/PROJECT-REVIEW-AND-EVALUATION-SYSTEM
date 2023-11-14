import imp
from flask import Flask,render_template,url_for,flash,redirect,request,session,send_file
from students.forms import UploadFileForm,RegistrationForm,LoginForm,ReplyFileForm,guideloginform,guideRegistrationForm,hodloginform,hodRegistrationForm,UploadFileFormhod
from students import app,db,bcrypt
import os
from students.models import User,Abstracts,Upload,Reply,Userguide,Userhod,Abstractshod,Replyhod,Final
from werkzeug.utils import secure_filename
from wtforms import FileField, SubmitField
from flask_login import login_user,current_user,logout_user,login_required
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
import csv

from students.dataset import Dataset
from students.utils import timer
from students.sentence_similarity import SentenceSimilarity


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/search")
def search():
    return render_template('search.html')


@app.route('/search', methods=["GET", "POST"])
def search_request():
    
    with open('data.csv','w',newline='') as csvfile:
        csvw=csv.writer(csvfile,delimiter=',')
        r=Final.query.all()
        for x in r:
            csvw.writerow([x.title,x.teamname])

    dataset = timer(Dataset, 'data.csv')
    sentence_sim = timer(SentenceSimilarity, dataset=dataset)

    query = request.form["input"]
    most_sim_docs = sentence_sim.get_most_similar(query)

    hits = [{"body": doc} for doc in most_sim_docs]
    d = []
    for title in hits:       
        dt = {}
        qs = Replyhod.query.filter_by(title=title['body']).first()
        # tag = title['body']
        # search = "%{}%".format(tag)        
        # qs = Replyhod.query.filter(Replyhod.title.like(search)).all()
        # print(f"Team {qs} and Title {title['body']}") 
        # dt.update({'title':title})
        if qs:
            print("Team is:",qs.teamname)
            title.update({'teamname':qs.teamname})
        d.append(title)
    
    res = {}
    res['total'] = len(most_sim_docs)
    # print("AM from Db and Dataset",d)
    res['hits'] = d # hits

    return render_template('results.html', res=res)









@app.route("/home/guideregister",methods=['GET','POST'])
def forgotgp():
    if current_user.is_authenticated:
        return redirect(url_for('guidepage'))
    form=guideRegistrationForm()
    if form.validate_on_submit():
        userguide = Userguide(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(userguide)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('guidepage'))


    return render_template('guideregister.html',form=form)


@app.route("/home/teamregister",methods=['GET','POST'])
def forgottp():
    if current_user.is_authenticated:
        return redirect(url_for('student'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(teamname=form.teamname.data, guidename=form.guidename.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.teamname.data}!','success')
        return redirect(url_for('student'))
    return render_template('teamregister.html',form=form)

@app.route("/home/hodregister",methods=['GET','POST'])
def forgothp():
    if current_user.is_authenticated:
        return redirect(url_for('hodpage'))
    form=guideRegistrationForm()
    if form.validate_on_submit():
        userhod = Userhod(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(userhod)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('hodpage'))
    return render_template('hodregister.html',form=form)



@app.route("/results")
def results():
    return render_template('results.html')




@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/teamregister",methods=['GET','POST'])
def teamregister():
    if current_user.is_authenticated:
        return redirect(url_for('student'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(teamname=form.teamname.data, guidename=form.guidename.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.teamname.data}!','success')
        return redirect(url_for('student'))

    return render_template('teamregister.html',form=form)

@app.route("/home/studentlogin", methods=['GET', 'POST'])
def studentlogin():
    if current_user.is_authenticated:
        return redirect(url_for('student'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(teamname=form.teamname.data).first()
        if user and user.password==form.password.data:
            
            print("Team",user.teamname)
            session['tmname']=user.teamname
            session['st_guidename'] = user.guidename
            login_user(user,remember=form.remember.data)
            return redirect(url_for('student'))
        else:
            flash('Login Unsuccessful. Please check teamname and password', 'danger') 
            return redirect(url_for('teamregister'))
    return render_template('studentlogin.html',form=form)
 
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

@app.route("/home/studentlogin/student/upg",methods=['GET','POST'])
def upg():
    form=UploadFileForm()
    if request.method == 'POST':
        file = request.files['file']
        abs = Abstracts(teamname=form.teamname.data,guidename=form.guidename.data,title=form.project.data,technology=form.domain.data,filename=file.filename,data=file.read())
        db.session.add(abs)
        db.session.commit()
        return f'Uploaded: {file.filename}'       
    return render_template('upg.html',form=form)


@app.route("/home/studentlogin/student/uph",methods=['GET','POST'])
def uph():
    form=UploadFileFormhod()
    if request.method == 'POST':
        file = request.files['file']
        absh = Abstractshod(
            teamname=form.teamname.data,
            hodname=form.hodname.data,
            guidename=form.guidename.data,
            title=form.project.data,
            technology=form.domain.data,
            filename=file.filename,
            data=file.read())
        db.session.add(absh)
        db.session.commit()
        return f'Uploaded: {file.filename}'
    # form.update({'guidename':session['st_guidename'] })  
    return render_template('uph.html',form=form)


@app.route("/home/studentlogin/student/vrg")
def  vrg():
    #data=Abstracts.query.filter_by(guidename='g1').all()
    #current_user="d1"
    current_user=session['tmname']
    data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname==current_user) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).filter_by(teamname=current_user).all()
    return render_template('vrg.html',data=data)

@app.route("/home/studentlogin/student/download_files/<id>",methods=['GET','POST'])
def download_files(id):    
    abs_qs=Abstracts.query.filter_by(id=id).first()    
    return send_file(BytesIO(abs_qs.data), attachment_filename=abs_qs.filename, as_attachment=True)


@app.route("/home/studentlogin/student/delete_replay_guide/<id>")
def delete_replay_guide(id):
    # Reply.query.filter_by(id=id).delete()
    qs = Reply.query.filter_by(id=id).first()
    qs_hod = Abstracts.query.filter_by(teamname=qs.teamname,title=qs.title,filename=qs.filename).first()

    Reply.query.filter(Reply.id==id).delete()
    Abstracts.query.filter(Abstracts.id==qs_hod.id).delete()

    db.session.commit()
    current_user=session['tmname']
    data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname==current_user) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).filter_by(teamname=current_user).all()
    return render_template('vrg.html',data=data)

@app.route("/home/studentlogin/student/upload_hod_simplyfy/<id>")
def upload_hod_simplyfy(id):
    qs = Abstracts.query.filter_by(id=id).first()
    qs_hod = Abstractshod.query.filter_by(teamname=qs.teamname,guidename=qs.guidename,title=qs.title,technology=qs.technology,filename=qs.filename).first()
    print(qs_hod)
    if qs_hod:
        flash('Already Uploaded')
    else:
        absh = Abstractshod(
            teamname=qs.teamname,
            hodname='My HOD',
            guidename=qs.guidename,
            title=qs.title,
            technology=qs.technology,
            filename=qs.filename,
            data=qs.data)
        db.session.add(absh)
        db.session.commit()

    current_user=session['tmname']
    data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname==current_user) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).filter_by(teamname=current_user).all()
    return render_template('vrg.html',data=data)

@app.route("/home/studentlogin/student/upload_hod_final/<id>")
def upload_hod_final(id):
    qs = Abstractshod.query.filter_by(id=id).first()
    qs_hod=Final.query.filter_by(teamname=qs.teamname).first()
    print(qs_hod)
    if  qs_hod:
            flash("Already Uploaded")
    else:
            absh = Final(
                teamname=qs.teamname,
                guidename=qs.guidename,
                title=qs.title,
                technology=qs.technology,
                filename=qs.filename,
                data=qs.data)
            db.session.add(absh)
            db.session.commit()

    current_user=session['tmname']
    data=db.session.query(Abstractshod,Replyhod).join(Abstractshod,(Replyhod.teamname==Abstractshod.teamname==current_user) & (Replyhod.title==Abstractshod.title) & (Replyhod.filename==Abstractshod.filename)).filter_by(teamname=current_user).all()
    return render_template('vrh.html',data=data)








@app.route("/home/studentlogin/student/vrh")
def  vrh():
    current_user=session['tmname']
    data=db.session.query(Abstractshod,Replyhod).join(Abstractshod,(Replyhod.teamname==Abstractshod.teamname==current_user) & (Replyhod.title==Abstractshod.title) & (Replyhod.filename==Abstractshod.filename)).filter_by(teamname=current_user).all()
    return render_template('vrh.html',data=data)

@app.route("/home/studentlogin/student/download_filevrh/<id>",methods=['GET','POST'])
def download_filevrh(id):    
    abs_qs=Abstractshod.query.filter_by(id=id).first()    
    return send_file(BytesIO(abs_qs.data), attachment_filename=abs_qs.filename, as_attachment=True)
 


   
@app.route("/guideregister",methods=['GET','POST'])
def guideregister():
    if current_user.is_authenticated:
        return redirect(url_for('guidepage'))
    form=guideRegistrationForm()
    if form.validate_on_submit():
        userguide = Userguide(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(userguide)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('guidepage'))

    return render_template('guideregister.html',form=form)



@app.route("/home/guidelogin", methods=['GET', 'POST'])
def guidelogin():
    if current_user.is_authenticated:
        return redirect(url_for('guidepage'))
    form=guideloginform()
    if form.validate_on_submit():
        userguide=Userguide.query.filter_by(username=form.username.data).first()
        
        if userguide and userguide.password==form.password.data:
            session['tmname']=userguide.username
            login_user(userguide,remember=form.remember.data)
            return redirect(url_for('guidepage'))
        else:
            flash('Login Unsuccessful. Please check teamname and password', 'danger') 
            return redirect(url_for('guideregister'))
    return render_template('guidelogin.html',form=form)


@app.route("/home/guidelogin/guidepage", methods=['GET', 'POST'])
def guidepage():
    if request.method == 'GET':
        return render_template('guidepage.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'View Project Details':
             redirect(url_for('vpd.html'))

        elif  request.form['submit'] == 'View project Status':
            return render_template('vpds.html')
       
        return render_template('guidepage.html')



@app.route("/home/guidelogin/guidepage/vpd",methods=['GET','POST'])
def vpd():
     #data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).all()
     current_user=session['tmname']
     data=Abstracts.query.filter_by(guidename=current_user).all()
     #data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname==current_user) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).filter_by(guidename=current_user).all()
     return render_template('vpd.html',data=data)

@app.route("/home/guidelogin/guidepage/vpd/download_file/<id>",methods=['GET','POST'])
def download_file(id):    
    abs_qs=Abstracts.query.filter_by(id=id).first()    
    return send_file(BytesIO(abs_qs.data), attachment_filename=abs_qs.filename, as_attachment=True)


     

@app.route("/home/guidelogin/guidepage/vps",methods=['GET','POST'])
def vps():
     current_user=session['tmname']
     data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).filter_by(guidename=current_user).all()
     
     #data=Abstracts.query.filter_by(guidename=current_user).all()
     #data=Abstracts.query.filter_by(guidename='g1').all()
     
     return render_template('vps.html',data=data)



@app.route("/home/guidelogin/guidepage/vpd/name/<id>",methods=['GET','POST'])
def name(id):
    return render_template('name.html',abstracts=Abstracts.query.filter_by(id=id))




@app.route("/home/guidelogin/guidepage/vpd/name/appr_rej/<id>",methods=['GET','POST'])
def appr_rej(id):
    form=ReplyFileForm()
    if form.validate_on_submit():
            if form.status.data=='A':
                val="Approve"
            if form.status.data=='R':
                val="Reject"
            data=Abstracts.query.filter_by(id=id).all()
            teamname=data[0].teamname
            title=data[0].title
            filename=data[0].filename
            guidereply = Reply(reply=form.reply.data,status=val,teamname=teamname,title=title,filename=filename)
            db.session.add(guidereply)
            db.session.commit()
            return redirect(url_for('vpd'))


    return render_template('appr_rej.html',abstracts=Abstracts.query.filter_by(id=id),form=form)



@app.route("/table/appr_rej/<id>/appr",methods=['GET','POST'])
def appr(id):
    return render_template('appr.html',abstracts=Abstracts.query.filter_by(id=id))


@app.route("/table")
def table():
    data=db.session.query(User,Abstracts).join(Abstracts,User.teamname==Abstracts.teamname).all()
    data1=User.query.all()
    data2=Abstracts.query.all()
    #data=User.join(Abstracts,User.teamname==Abstracts.teamname)
    return render_template('table.html',data=data,data1=data1,data2=data2)

@app.route("/hodregister",methods=['GET','POST'])
def hodregister():
    if current_user.is_authenticated:
        return redirect(url_for('hodpage'))
    form=guideRegistrationForm()
    if form.validate_on_submit():
        userhod = Userhod(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(userhod)
        db.session.commit()
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('hodpage'))

    return render_template('hodregister.html',form=form)




@app.route("/home/hodlogin", methods=['GET', 'POST'])
def hodlogin():
    if current_user.is_authenticated:
        return redirect(url_for('hodpage'))
    form=hodloginform()
    if form.validate_on_submit():
        userhod=Userhod.query.filter_by(username=form.username.data).first()
        
        if userhod and userhod.password==form.password.data:
            session['temname']=userhod.username
            login_user(userhod,remember=form.remember.data)
            return redirect(url_for('hodpage'))
        else:
            flash('Login Unsuccessful. Please check teamname and password', 'danger') 
            return redirect(url_for('hodregister'))
    return render_template('hodlogin.html',form=form)


@app.route("/home/hodlogin/hodpage", methods=['GET', 'POST'])
def hodpage():
    if request.method == 'GET':
        return render_template('hodpage.html')
    elif request.method == 'POST':
        if request.form['submit'] == 'View Project Details':
             redirect(url_for('vpdh.html'))
             #return render_template('vpdh.html')
        elif  request.form['submit'] == 'View Project Status':
            return render_template('vpsh.html')
       

        return render_template('hodpage.html')


@app.route("/home/hodlogin/hodpage/vpdh",methods=['GET','POST'])
def vpdh():
     current_user=session['temname']
     #data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).all()
     #data=Abstractshod.query.filter_by(hodname=current_user).all()
     data=Abstractshod.query.filter_by().all()
     return render_template('vpdh.html',data=data)


@app.route("/home/hodlogin/hodpage/vpdh/download_fileh/<id>",methods=['GET','POST'])
def download_fileh(id):    
    abs_qs=Abstractshod.query.filter_by(id=id).first()    
    return send_file(BytesIO(abs_qs.data), attachment_filename=abs_qs.filename, as_attachment=True)



@app.route("/home/hodlogin/hodpage/vpsh",methods=['GET','POST'])
def vpsh():
     #current_user=session['tmname']
     data=db.session.query(Abstractshod,Replyhod).join(Abstractshod,(Replyhod.teamname==Abstractshod.teamname) & (Replyhod.title==Abstractshod.title) & (Replyhod.filename==Abstractshod.filename)).all()
     
     #data=Abstracts.query.filter_by(guidename=current_user).all()
     #data=Abstracts.query.filter_by(guidename='g1').all()
     
     return render_template('vpsh.html',data=data)






@app.route("/home/hodlogin/hodpage/vpdh/nameh/<id>",methods=['GET','POST'])
def nameh(id):
    return render_template('nameh.html',abstracts=Abstractshod.query.filter_by(id=id))



@app.route("/home/hodlogin/hodpage/vpdh/nameh/appr_rejh/<id>",methods=['GET','POST'])
def appr_rejh(id):
    form=ReplyFileForm()
    if form.validate_on_submit():
            if form.status.data=='A':
                val="Approve"
            if form.status.data=='R':
                val="Reject"
            data=Abstractshod.query.filter_by(id=id).all()
            teamname=data[0].teamname
            title=data[0].title
            filename=data[0].filename
            hodreply = Replyhod(reply=form.reply.data,status=val,teamname=teamname,title=title,filename=filename)
            db.session.add(hodreply)
            db.session.commit()
            return redirect(url_for('vpdh'))


    return render_template('appr_rejh.html',abstracts=Abstractshod.query.filter_by(id=id),form=form)



@app.route("/home/studentlogin/student/delete_replay_hod/<id>")
def delete_replay_hod(id):
    # Reply.query.filter_by(id=id).delete()
    Replyhod.query.filter(Replyhod.id==id).delete()
    db.session.commit()
    current_user=session['tmname']
    data=db.session.query(Abstractshod,Replyhod).join(Abstractshod,(Replyhod.teamname==Abstractshod.teamname==current_user) & (Replyhod.title==Abstractshod.title) & (Replyhod.filename==Abstractshod.filename)).filter_by(teamname=current_user).all()
    return render_template('vrh.html',data=data)









@app.route("/home/project_status1/reply_by_hod")
def reply_by_hod():
    return render_template('reply_by_hod.html')

@app.route("/home/project_status/reply_by_guide")
def reply_by_guide():
    return render_template('reply_by_guide.html')





@app.route("/home/")
def abg():
    return render_template('abg.html')

@app.route('/guide')
def guide():
    if current_user.is_authenticated:
        return redirect(url_for('guidepage'))
    form=guideloginform()
    if form.validate_on_submit():
        userguide=Userguide.query.filter_by(username=form.username.data).first()
        if userguide and userguide.password==form.password.data:
            login_user(userguide,remember=form.remember.data)
            return redirect(url_for('guidepage'))
        else:
            flash('Login Unsuccessful. Please check teamname and password', 'danger') 
            return redirect(url_for('guideregister'))
    return render_template('guidelogin.html',form=form)

@app.route('/hod')
def hod():
    if current_user.is_authenticated:
        return redirect(url_for('hodpage'))
    form=hodloginform()
    if form.validate_on_submit():
        userhod=Userhod.query.filter_by(username=form.username.data).first()
        if userhod and userhod.password==form.password.data:
            login_user(userhod,remember=form.remember.data)
            return redirect(url_for('hodpage'))
        else:
            flash('Login Unsuccessful. Please check teamname and password', 'danger') 
            return redirect(url_for('hodregister'))
    return render_template('hodlogin.html',form=form)


@app.route("/home/hodlogin/hodpage/vd",methods=['GET','POST'])
def vd():
     #data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).all()
    
     data=Final.query.all()
     #data=db.session.query(Abstracts,Reply).join(Abstracts,(Reply.teamname==Abstracts.teamname==current_user) & (Reply.title==Abstracts.title) & (Reply.filename==Abstracts.filename)).filter_by(guidename=current_user).all()
     return render_template('vd.html',data=data)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/edit")
@login_required
def edit():
    return render_template('edit.html')

@app.route("/home/guidepage",methods=['GET','POST'])
def backguidepage1():
    return render_template('guidepage.html')


@app.route("/home/hodpage",methods=['GET','POST'])
def backhodpage2():
    return render_template('hodpage.html')


@app.route("/home",methods=['GET','POST'])
def backstudent():
    return render_template('home.html')


@app.route("/home/student",methods=['GET','POST'])
def backvrg():
    return render_template('home.html')

@app.route("/home/student",methods=['GET','POST'])
def backvrh():
    return render_template('home.html')

@app.route("/home",methods=['GET','POST'])
def backguidepage():
    return render_template('home.html')


@app.route("/home",methods=['GET','POST'])
def backhodpage():
    return render_template('home.html')

@app.route("/home/guidelogin/guidepage/vpd",methods=['GET','POST'])
def backname():
    return render_template('vpd.html')

@app.route("/home/hodlogin/hodpage/vpdh",methods=['GET','POST'])
def backnameh():
    return render_template('vpdh.html')


@app.before_first_request
def create_tables():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
    db.create_all()





  

