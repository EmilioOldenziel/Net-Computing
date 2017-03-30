from __future__ import unicode_literals, division

from flask import render_template

from . import app, db

@app.route('/', methods=['GET'])
def view_home():
    return render_template('index.html')
