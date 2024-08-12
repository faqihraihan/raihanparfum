from flask import Blueprint, render_template

dashb = Blueprint('dashb', __name__)

@dashb.route('/')
def dashboard():
    return render_template('dashboard/dashboard.html')