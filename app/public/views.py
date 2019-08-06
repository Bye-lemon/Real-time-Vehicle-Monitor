# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_socketio import emit

from app.extensions import login_manager, socketio
from app.public.forms import LoginForm
from app.user.forms import RegisterForm
from app.user.models import User, RawData
from app.model.kmeans import predict
from app.utils import flash_errors

import time
import json

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(id=time.time(), username=form.username.data, email=form.email.data, password=form.password.data,
                    active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)


@socketio.on('wsrequest')
def run():
    raw_data = RawData.query.limit(100).all()
    cars = raw_data[0].gear
    real_data = raw_data[: 40] if len(raw_data) > 40 else raw_data
    low, mid, high = predict(real_data)
    ret_dict = dict()
    for index, item in enumerate(raw_data):
        ret_dict[str(index)] = {
            "gear": item.gear,
            "handbreak": item.handbreak,
            "maxrpm": item.maxrpm,
            "rpm": item.rpm,
            "speed": item.speed,
            "timestamp": time.time(),
            "pos_x": float(item.pos_x),
            "pos_y": float(item.pos_y),
            "pos_z": float(item.pos_z),
            "aa_x": item.aa_x,
            "aa_y": item.aa_y,
            "aa_z": item.aa_z,
            "av_x": item.av_x,
            "av_y": item.av_y,
            "av_z": item.av_z,
            "la_x": item.la_x,
            "la_y": item.la_y,
            "la_z": item.la_z,
            "lv_x": item.lv_x,
            "lv_y": item.lv_y,
            "lv_z": item.lv_z
        }
    pred = {
        "low": low,
        "mid": mid,
        "high": high
    }
    ret = json.dumps(ret_dict)
    time_str = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    emit('wsresponse', {
        "owner": current_user.username,
        "time": time_str,
        "data": ret,
        "car": cars,
        "pred": pred
    })
