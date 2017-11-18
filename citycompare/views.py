from flask import render_template
from citycompare import flask_app

@flask_app.route('/')
def index():
    return render_template(
        'index.html'
    )
