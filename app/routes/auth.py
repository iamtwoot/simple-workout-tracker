from flask import Blueprint, render_template, flash, redirect, url_for
from app.forms.login import LoginForm
from app.extensions import db
from app.models import User
from flask_login import login_user, current_user, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        password = form.password.data
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))

        if not user:
            flash("No username found", "error")

        elif not user.check_password_hash(password):
            flash("Invalid password, try again.", "error")

        else:
            login_user(user)
            return redirect(url_for('workouts'))

    return render_template("auth/login.html", form=form)
