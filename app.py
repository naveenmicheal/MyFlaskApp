from flask import Flask, request, url_for, redirect,session
from flask import render_template
from flask_mysqldb import MySQL
from form import register_form
app = Flask(__name__)
mysql = MySQL(app)

app.secret_key = 'MyKey123'
app.config['SECRET_KEY'] = '112345678'

# DB config
app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='password'
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

# ---------------------------------------Login----------------------------------------

@app.route('/login', methods=['POST','GET'])
def login():
	if request.method =='POST':
		email = request.form['email']
		e_pass = request.form['password']
		# print('{} {}'.format(email, e_pass))
		# Mysql connction

		cur = mysql.connection.cursor()
		result = cur.execute("""SELECT * FROM user WHERE email =%s""",[email])
		if result>0:
			data = cur.fetchone()
			print(data)
			# Check password
			dbpassword = data['password']
			username = data['name']
			if e_pass == dbpassword:
				app.logger.info("Password Matched")
				session['logged_in'] = True
				session['user'] = username
				return redirect(url_for('profile'))
			else:
				error = "Invalid Login"
				return render_template('login.html', error = error)
		else:
			error = "No user Found "
			return render_template('login.html', error = error)
		cur.close()	
		
	else:
		return render_template('login.html')	
# ------------------------------Profile--------------------------------------

@app.route('/profile')
def profile():
	return render_template('profile.html')

# Logout
@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('login'))



















if __name__ == '__main__':
    app.run(debug = True, host ='0.0.0.0', port =3333)

			