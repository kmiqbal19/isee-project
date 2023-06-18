from flask import render_template, request, session, redirect, url_for, flash
from shop import app, db, bcrypt
from .forms import RegistrationForm, LoginForm
from .models import User
from shop.products.models import Addproduct,Category,Brand

# ---- ROUTES ------
@app.route('/')
def home():
    admin_there = True
    if 'email' not in session:
        admin_there = False
    products = Addproduct.query.all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('admin/index.html', title='Buy Here', admin_there=admin_there ,products=products, brands=brands, categories=categories)

@app.route('/admin')
def admin():
    admin_there = True
    if 'email' not in session:
        admin_there = False
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.all()
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    categories = Category.query.join(Addproduct, (Category.id == Addproduct.category_id)).all()
    return render_template('admin/admin.html', title='Admin page', products=products, brands=brands, categories=categories , admin_there=admin_there)


@app.route('/brands')
def brands():
    admin_there = True
    if 'email' not in session:
        admin_there = False
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='brands', brands=brands, admin_there=admin_there)


@app.route('/categories')
def categories():
    admin_there = True
    if 'email' not in session:
        admin_there = False
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/category.html', title='categories',categories=categories, admin_there=admin_there)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data, username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Registration page")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["email"] = form.email.data
            flash(
                f'Welcome {form.email.data}, You are logged in as admin now!', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong credentials. Please try again', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html', form=form, title="Login page")
