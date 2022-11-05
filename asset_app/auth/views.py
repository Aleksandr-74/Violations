from flask import Blueprint, session, flash, redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from asset_app import db, login_manager, app
from asset_app.auth.models import RegistrationForm, LoginForm, User

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/home')
def home():
    return render_template('index.html')


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if session.get('username'):
        flash('Вы уже авторизированы!', 'success')
        return redirect(url_for('auth.home', username='username'))

    elif form.validate_on_submit():
        try:
            user = User(form.username.data, form.password.data)
            with app.app_context():
                db.create_all()
                db.session.add(user)
                db.session.flush()
                db.session.commit()
            return redirect(url_for('auth.login', username='username'))

        except Exception as e:
            db.session.rollback()
            print(f'Ошибка добавления в БД: {e}')
    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(username= form.username.data).first()
            if user and check_password_hash(user.pwdhash, form.password.data):

                rm = True if request.form.get('remainme') else False
                login_user(user, remember=rm)
                next_page = request.args.get('next')
                flash('Вы успешно авторизовались!', 'success')
                if next_page:
                    redirect(url_for(next_page))
                return redirect(url_for('auth.home'))

            else:
                flash('Неверное имя пользователя или пароль', 'danger')
                return render_template('login.html', form=form)

        elif form.errors:
            flash(form.errors, 'danger')

        return render_template('login.html', form=form)
    else:
        return redirect(url_for('auth.profile'))


@auth.after_request
def redirect_to_signin(response):
    if response.status == 404:
        return redirect(url_for('login') + '?next=' + request.url)
    return response


@auth.route('/profile')
@login_required
def profile():
    user = current_user
    print(user)
    return render_template('profile.html', user=user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы!', 'success')
    return redirect(url_for('auth.login'))


