from flask import Flask, render_template, url_for
from gevent.pywsgi import WSGIServer
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(host='127.0.0.1', user='root', password='root', database='college')


@app.route('/mark/<int:id>')
def index(id):
	cur = db.cursor()
	db.commit()  # Magic commit, without it server got old data from DB. IDK why :)
	cur.execute('select FK_discipline, discipline_name from v_stundent_lesson where id_student=%s;', (id,))
	lessons = cur.fetchall()
	marks = []

	for el in lessons:
		cur.execute('select digital_name from v_students_mark where FK_discipline=%s and id_student=%s\
			order by PK_student_mark;', (el[0], id))
		marks.append((el[1], cur.fetchall()))

	return render_template('all_mark.html', marks=marks)


if __name__ == '__main__':
	# app.run(port=80, debug=True)
	http_server = WSGIServer(('127.0.0.1', 80), app)
	http_server.serve_forever()
