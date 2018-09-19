from flask import Flask, request, url_for, redirect,session
from flask import render_template
from functools import wraps
from flask_mysqldb import MySQL
from form import register_form,post_form
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
		return redirect(url_for('login'))
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
		data123 = request.args.get('invaliderror')
		return render_template('login.html', data123 = data123)	

#check the user is logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args ,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			invaliderror = "You must Login to Continue"
			session['invaliderror'] = invaliderror
			return redirect(url_for('login',invaliderror = invaliderror))
	return wrap		
 
# ------------------------------Profile--------------------------------------

@app.route('/profile',methods =['POST','GET'])
@is_logged_in
def profile():
	postinfo = request.args.get('postinfo')
	return render_template('profile.html', postinfo = postinfo)

#-------------------------------Add Post------------------------------------

@app.route('/add_post', methods = ['POST','GET'])
@is_logged_in
def add_post():
	form = post_form(request.form)
	if request.method =='POST' and form.validate():
		title = request.form['title']
		author = session['user']
		content = request.form['content']
		print(title)
		print(author)
		print(content)
		cur = mysql.connection.cursor()
		cur.execute("""INSERT INTO posts (title,author,content)
		 VALUES(%s,%s,%s)""",(title, author,content))
		mysql.connection.commit()
		cur.close()

		postinfo = "Your Recent Contennt is Added"
		app.logger.info(postinfo)
		return redirect(url_for('profile',postinfo = postinfo))
	else:
		app.logger.info("Form Invalid")
		return render_template('add_post.html', form = form)	

# Logout
@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(debug = True, host ='0.0.0.0', port =3333)

			