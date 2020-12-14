#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, make_response
from gevent.pywsgi import WSGIServer
from hashlib import sha3_256 as sha3
import mysql.connector
import db_config

app = Flask(__name__)
db = mysql.connector.connect(**db_config.db)


def hash(text):
	return sha3(str(text).encode('utf-8')).hexdigest()


def acc(func):
	def wrap(*a, **ka):
		auth_id = request.cookies.get('auth_id', None)
		if auth_id:
			cur = db.cursor(buffered=True)
			cur.execute('select * from session where id=%s;', (auth_id,))
			session = cur.fetchone()
			if session:
				return func(*a, session=session, **ka)
		return redirect('/')
	wrap.__name__ = func.__name__
	return wrap


@app.route('/')
def index():
	cur = db.cursor(buffered=True)
	auth = request.cookies.get('auth', None)
	auth_id = request.cookies.get('auth_id', None)
	if auth and auth_id:
		cur.execute('select * from session where id=%s;', (auth_id,))
		session = cur.fetchone()
		if session:
			ip = request.remote_addr
			agent = request.user_agent.string
			cur.execute('select password from `dovidnyuk_students` where id_student=%s;', (session[1],))
			password = cur.fetchone()
			if password:
				_hash = hash(hash(password[0]+ip)+agent)
				if ip == request.remote_addr and agent == request.user_agent.string and auth == _hash:
					return mark(session[1])
	return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
	try:
		password = hash(request.form['pass'])
		login = request.form['login']

		cur = db.cursor(buffered=True)
		cur.execute('select password from `dovidnyuk_students` where id_student=%s;', (login,))
		if password == cur.fetchone()[0]:
			ip = request.remote_addr
			agent = request.user_agent.string
			session_hash = hash(hash(password+ip)+agent)
			cur.execute('insert into session values(null, %s, %s, %s, %s);', (login, ip, agent, session_hash))
			db.commit()
			cur.execute('select id from session where id_user=%s and ip=%s and agent=%s;', (login, ip, agent))
			session_id = cur.fetchone()[0]
			resp = make_response(redirect('/'))
			resp.set_cookie('auth', str(session_hash), max_age=432000)
			resp.set_cookie('auth_id', str(session_id), max_age=432000)
			return resp
	except KeyError:
		pass
	return redirect('/')


@app.route('/exit')
@acc
def _exit(session):
	cur = db.cursor()
	resp = make_response(redirect('/'))
	resp.set_cookie('auth', '', max_age=259200)
	resp.set_cookie('auth_id', '', max_age=259200)
	cur.execute('delete from session where id=%s;', (session[0],))
	db.commit()
	return resp


@app.route('/mark/<int:student_id>')
def mark(student_id):
	cur = db.cursor()
	db.commit()  # Magic commit, without it server got old data from DB. IDK why :)
	cur.execute('select FK_discipline, discipline_name from v_stundent_lesson where id_student=%s;', (student_id,))
	lessons = cur.fetchall()
	marks = []

	for el in lessons:
		cur.execute('select digital_name from v_students_mark where FK_discipline=%s and id_student=%s\
			order by PK_student_mark;', (el[0], student_id))
		marks.append((el[1], cur.fetchall()))

	return render_template('all_mark.html', marks=marks)


if __name__ == '__main__':
	#app.run(port=80, debug=True)
	http_server = WSGIServer(('127.0.0.1', 80), app)
	http_server.serve_forever()
