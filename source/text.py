from datetime import datetime
from flask import Flask, render_template, session, url_for, redirect, flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lihas'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class textFrom(Form):
	t = TextAreaField('Write the text : ', validators=[Required()])
	name = StringField('Name of text file : ', validators=[Required()])
	submit = SubmitField('Submit')
	
def write_to_file(t,name):
	if name[-4:] == '.txt':
		name = name[:-4]
	name = name+'.txt'
	f = open(name,'w')
	f.write(t)
	f.close()
	
@app.errorhandler
def page_not_found(e):
	return render_template('404.html')
	
@app.errorhandler
def internal_server_error(e):
	return render_template('500.html')

@app.route('/', methods=['GET', 'POST'])
def index():
	form = textFrom()
	t = ''
	name = ''
	if(form.validate_on_submit()):
		t = form.t.data
		name = form.name.data
		write_to_file(t, name)
		#add your text manipulating function here to change the contents of file and reassign 't' and 'name'
		return render_template('done.html', t = t, name = name, current_time = datetime.utcnow())
	return render_template('index.html', form = form, t = t, name = name, current_time = datetime.utcnow())

if __name__ == '__main__':
	app.debug = True
	manager.run()
