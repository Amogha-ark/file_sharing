from flask import Flask, render_template, url_for, flash, redirect,request,session,send_file
from flask_sqlalchemy import SQLAlchemy
import datetime
from io import BytesIO
# import yaml
import random
import string
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///filesdb.sqlite"
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db = SQLAlchemy(app)
global glid
glid=0
class filesdata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uni_id = db.Column(db.String(100))
    name = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

    def __init__(self,uni_id,name,data):
        self.uni_id = uni_id
        self.name=name
        self.data=data

def generate_string(n,r,val):
    st=''
    for i in range((n//2)+1):
        v=val%10
        st+=r[v]
        val=val//10
    let =''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
    return let+st

def get_unique_id():
    res=filesdata.query.all()
    arr=[]
    if res:
        arr=[i.uni_id for i in res]
        v=datetime.datetime.now()
        m=v.strftime("%H%S%M%f")
        o=len(m)
        all_letters=string.ascii_letters
        st=generate_string(o,all_letters,int(m,base=10))
        for i in range(255):
            if st not in arr:
                break
            else:
                st=generate_string(o,all_letters,int(m,base=10))
        return st
            
    else:
        v=datetime.datetime.now()
        m=v.strftime("%H%S%M%f")
        o=len(m)
        all_letters=string.ascii_letters
        st=generate_string(o,all_letters,int(m,base=10))
        return st


@app.route("/home")
def home():
    res = filesdata.query.all()
    print("home")
    return redirect(url_for("user"))


@app.route("/user/<string:v>", methods=['GET', 'POST'])
def user(v):
    
    # print(v)
    # global glid
    print("enetred",glid)
    # v=glid
    # glid=0
    ss=v
    print(ss)
    if v:
        return render_template("user.html",data=ss)
    else:

        return render_template('user.html')
@app.route("/filenew",methods=["POST","GET"])
def filenew():
    global glid
    if glid:
        my_id=glid
    else:
        my_id = get_unique_id()
        glid=my_id
    # my_id = get_unique_id()
    if request.method=="POST":
        # print(request.files)
        # print(request.files)
        # print("---------Enetred----------")
        # my_id = get_unique_id()
        # glid=0
        newfile = request.files['myfile']
        print(newfile.filename)
        
        print("id genereted --------------------",my_id)
        newobj=filesdata(my_id,newfile.filename,newfile.read())
        db.session.add(newobj)
        db.session.commit()
        print(filesdata.query.all())
        return render_template("user.html")
    else:
        # print(res)
        print("Pleas select a file")
        return render_template("filenew.html",data=my_id)

@app.route("/download/<string:li>" ,methods=["POST","GET"])
def download(li):
    global glid
    glid =0 
    # res=filesdata.query.all()
    # print(res[0].uni_id)

    res=filesdata.query.filter_by(uni_id=li).first()
    
    if res:
        given_name=res.name
    else:
        given_name="Not found"
    if request.method=="POST":

        filesdata.query.filter_by(uni_id=li).delete()
        db.session.commit()
        if res:
            print("enetred")
            return send_file(BytesIO(res.data),attachment_filename=res.name,as_attachment=True)
            # return render_template("download.html",data="Downloaded")
        else:
            return render_template("download.html",data="Not Valid ")
    else:
        return render_template("download.html",data=given_name)
    return "success"
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)