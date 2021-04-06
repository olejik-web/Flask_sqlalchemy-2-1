from datetime import datetime
from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.departments import Department
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    login_or_mail = StringField('Login / email', 
                                     validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = StringField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])    
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

    
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_session.global_init("db/mars.db")
    db_sess = db_session.create_session()
    jobs = [job for job in db_sess.query(Jobs).all()]
    users = [user for user in db_sess.query(User).all()]
    return render_template('works_journal.html', title='Journal works', 
                           jobs=jobs, users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_session.global_init("db/mars.db")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.login_or_mail.data     
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/register')
    return render_template('register_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    db_session.global_init("db/mars.db")
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def main():
    db_session.global_init("db/mars.db")
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    db_sess.add(user)
    db_sess.commit() 
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()


'''@app.route('/training/<prof>')


def training(prof):
    return render_template('training.html', prof=prof)'''

