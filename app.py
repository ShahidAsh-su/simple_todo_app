from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import AddTask


app = Flask(__name__)
app.config['SECRET_KEY'] = "b295a96745f08b9d71cfdd3947ded9ea"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class Tasks(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	task = db.Column(db.String(120),nullable=False,unique=True)
	time = db.Column(db.String(120),default=datetime.utcnow())

	def __repr__(self):
		return '<User %r>' % self.task

		

# todo = [
# 	{'task':'Do coding','time': datetime.utcnow()},
# 	{'task':'Do Dishes','time': datetime.utcnow()}
# ]

@app.route('/',methods=['GET','POST'])
def home():
	addTask = AddTask()
	if request.method == 'POST':
		task_name = addTask.task.data
		task = Tasks(task = task_name)
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('home'))
	todo = Tasks.query.all()
	return render_template('home.html',todo = todo,addtask = addTask)

@app.route('/delete',methods=['GET','POST'])
def delete():
	task_name = request.form.get('task')
	task = Tasks.query.filter_by(task=task_name).first()
	db.session.delete(task)
	db.session.commit()
	return redirect(url_for('home'))


if __name__=='__main__':
	app.run(debug=True)