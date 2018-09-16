from flask import Flask, request, url_for, redirect
from flask import render_template
from flask_mysqldb import MySQL
from form import register_form, login
app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = 'MyKey123'
app.config['SECRET_KEY'] = '112345678'

# DB config
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] =''
app.config['MYSQL_DB'] ='flaskapp'
app.config['MYSQL_CURSORCLASS'] ='DictCursor' #For returning Dictionary type data



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
	form = register_form(request.form)
	print(form.validate())
	if request.method =='POST' and form.validate():
		print('Ok')
		name = form.name.data
		email = form.email.data
		password = form.password.data
		cur = mysql.connection.cursor()
		cur.execute("""INSERT INTO user (name,email,password)
						VALUES (%s, %s, %s)""",(name,email,password))
		mysql.connection.commit()
		cur.close()
		return redirect(url_for('index'))
	else:
		return render_template('register.html', form = form)		

























if __name__ == '__main__':
    app.run(debug = True, host ='0.0.0.0', port =3333)

			