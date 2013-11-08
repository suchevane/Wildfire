from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import string
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname=wftrainers user=Marava password=mickey69")
cur = conn.cursor()

@app.route('/add', methods=[POST])
def add_stuff():
    cur.execute("insert into test (id, data) values (%s, %s)",[request.form['id'], request.form['data']])
    cur.commit()
    flash('Someone cares about your opinion!  Haha, not really')
    return redirect(url_for('shit_form'))

@app.route('/')
def shit_form():
    return render_template('shit_form.html') 
