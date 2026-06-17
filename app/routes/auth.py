from flask import Blueprint, render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms.login import LoginForm, RegistrationForm
from app.extensions import db
from app.models import User
from flask_login import login_user, login_required, logout_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        password = form.password.data
        user = db.session.scalar(db.select(User).where(User.email == form.email.data))

        if not user:
            flash("User with this email is not found", "error")

        elif not check_password_hash(user.password_hash, password):
            flash("Invalid password, try again.", "error")

        else:
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for('main.home'))

    return render_template("auth/login.html", form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():

        user = db.session.scalar(db.select(User).where(User.email == form.email.data))
        if user:
            flash("Email address already exists", "error")
            return redirect(url_for('auth.register'))

        hash_and_salted_password = generate_password_hash(form.password.data)

        new_user = User(
            username=form.username.data,
            email = form.email.data,
            password_hash = hash_and_salted_password,
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('main.home'))

    return render_template("auth/register.html", form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('main.home'))