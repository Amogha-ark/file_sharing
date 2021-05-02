from flask import Flask, render_template, url_for, flash, redirect,request,session
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


db = yaml.load(open('db.yaml'))
#configure db

app.config['MYSQL_HOST']=  db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_db']
mysql=MySQL(app)
@app.route("/user", methods=['GET', 'POST'])
def user():
    
    if request.method=='POST':
        userdetails=request.form
        name=userdetails['name']
        number=userdetails['number']
        cur = mysql.connection.cursor()
        
        cur.execute("INSERT INTO auto(name,number) VALUES(%s,%s)",(name,number))
        mysql.connection.commit()
        cur.close()

    return render_template('user.html')
if __name__ == '__main__':
    app.run(debug=True)