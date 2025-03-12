from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect  # Import CSRF protection

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # query.get is legacy, might need to change to session.get

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            flash("Username already exists. Please choose a different one.", "error")
            raise ValidationError('That username already exists. Please choose a different one.')

class GroceryList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('grocery_lists', lazy=True))

    def __repr__(self):
        return f'<GroceryList {self.name}>'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    grocery_list_id = db.Column(db.Integer, db.ForeignKey('grocery_list.id'), nullable=False)

class GroceryListForm(FlaskForm):
    list_name = StringField('List Name', validators=[InputRequired(), Length(min=3, max=100)], render_kw={"placeholder": "Enter list name"})
    submit = SubmitField('Create List')


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField('Login')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
        else:
            flash("This account doesn't exist. Register below.", "error")
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    lists = GroceryList.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', lists=lists)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

@app.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    form = GroceryListForm()
    if form.validate_on_submit():
        new_list = GroceryList(list_name=form.list_name.data, user_id=current_user.id)
        db.session.add(new_list)
        db.session.commit()
        flash('List created successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_edit_list.html', form=form)

class ItemForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(min=1, max=100)], render_kw={"placeholder": "Item Name"})
    submit = SubmitField('Add Item')

@app.route('/add_item/<int:list_id>', methods=['GET', 'POST'])
@login_required
def add_item(list_id):
    list = GroceryList.query.get_or_404(list_id)
    if list.user != current_user:
        flash("You are not authorized to edit this list.", "error")
        return redirect(url_for('dashboard'))
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(name=form.name.data, grocery_list_id=list_id)
        db.session.add(new_item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_item.html', form=form, list=list)


if __name__ == "__main__":
    app.run(debug=True)
