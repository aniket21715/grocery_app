import datetime
import os
import json
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from flask import Flask, render_template, url_for, redirect,request, session ,flash 
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask import current_app as app
from flask_wtf import FlaskForm
from web.dbase import db
from web.model import User, Admin ,Product ,Section, Purchase
from wtforms import StringField, PasswordField, SubmitField ,FileField, IntegerField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from flask import jsonify


bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'cart' not in session:
    # Initialize an empty cart and store it in the session
           session['cart'] = json.dumps(dict())
    if request.method == "GET":
        user = current_user if current_user.is_authenticated else None
        #user = session.get("user")
        section = Section.query.all()
        sections_with_products = Section.query.options(db.joinedload(Section.products)).all()
        return render_template("home.html", user=user, signed=bool(user), sections = section , sections_with_products=sections_with_products)
    elif request.method == "POST":
        product_id, count = request.form["product"], request.form["count"]
        product = Product.query.filter_by(id = product_id).first()
       # 
        cart = json.loads(session["cart"])
        if product_id in cart:
            current = int(count) + int(cart[product_id])
            if current <= int(product.stock):
                cart[product_id] = str(int(cart[product_id]) + int(count))
        else:
            current = int(count)
            if current <= int(product.stock):
                cart[product_id] = count

        session["cart"] = json.dumps(cart)
        print(session["cart"])
        return redirect("/")
    
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                session["user"] = user.username
                return redirect('/')
    return render_template('login.html', form=form)

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username=form.username.data).first()
        if user:
            if (user.password, form.password.data):
                login_user(user)
                session['admin_id'] = user.id
                return redirect(url_for('dashboard'))
    return render_template('adminlogin.html', form=form)



@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/adminlogout', methods=['GET', 'POST'])
def adminlogout():
    session.clear()
    return redirect('/')

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route('/adminregister', methods=['GET', 'POST'])
def adminregister():
    form = AdminLoginForm()
    if form.validate_on_submit():
        # Check if the username is already taken
        existing_user = Admin.query.filter_by(username=form.username.data).first()
        if existing_user:
            return redirect(url_for('adminregister'))

        # Create a new admin user
        new_admin = Admin(username=form.username.data, password=form.password.data)
        db.session.add(new_admin)
        db.session.commit()

        # flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('adminlogin'))

    return render_template('adminregister.html', form=form)

@app.route("/dashboard")
def dashboard():
    section = Section.query.all()
    sections_with_products = Section.query.options(db.joinedload(Section.products)).all()
    admin_id = session.get('admin_id')
    admin = Admin.query.get(admin_id) if admin_id else None 
    return render_template("admin_dashboard.html", sections = section , sections_with_products=sections_with_products, admin=admin)
   
@app.route("/add_section", methods=['GET', 'POST'])
def create_section():

    if request.method == "GET":
            return render_template("add_section.html")
    elif request.method == "POST":
            name = request.form["name"]
            description = request.form.get("description")
            section = Section(name = name, description = description)
            db.session.add(section)
            db.session.commit()
            return redirect(url_for('dashboard'))
    return redirect("/")


@app.route("/edit_section/<section_id>", methods=['GET', 'POST'])
def edit_section(section_id):
    section = Section.query.filter_by(id = section_id).first()
    if request.method == "GET":
                return render_template("edit_section.html", section = section )
    elif request.method == "POST":
                name = request.form["name"]
                description = request.form.get("description", None)
                if name:
                    section.name = name
                if description:
                    section.description = description
                db.session.commit()
                return redirect(url_for("dashboard"))
    return redirect("/")

@app.route("/delete_section/<section_id>", methods = ["GET", "POST"])
def delete_section(section_id):
    if request.method == "GET":
                return render_template("delete_section.html")
    elif request.method == "POST":
                if "yes" in request.form:
                    section = Section.query.filter_by(id = section_id).first()
                    db.session.delete(section)
                    db.session.commit()
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for("dashboard"))
    return redirect("/")

@app.route("/add_product/<section_id>", methods=['GET', 'POST'])
def add_product(section_id):

    if request.method == "GET":
            return render_template("add_product.html")
    elif request.method == "POST":
            name = request.form["name"]
            description = request.form.get("description")
            stock = request.form.get("stock")
            price = request.form.get("price")
            img = request.files["img"]
            product = Product(name = name, description = description, stock = stock ,section_id= section_id, price=price)
            
            db.session.add(product)
            db.session.commit()
            img.save("./static/products/" + str(product.id) + ".png")
            return redirect(url_for('dashboard'))
    return redirect("/")

@app.route("/edit_product/<product_id>", methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.filter_by(id = product_id).first()
    if request.method == "GET":
                return render_template("edit_product.html", product=product)
    elif request.method == "POST":
                name = request.form["name"]
                description = request.form.get("description", None)
                stock = request.form.get("stock", None)
                price = request.form.get("price")
                img = request.files.get("img", None)
                if name:
                    product.name = name
                if description:
                    product.description = description
                if stock:
                    product.stock = stock
                if price:
                     product.price  = price
                db.session.commit()
                if img:
                    img.save("./static" + str(product.id) + ".png")
                return redirect(url_for("dashboard"))
    return redirect("/")

@app.route("/delete_product/<product_id>", methods = ["GET", "POST"])
def delete_product(product_id):
    if request.method == "GET":
                return render_template("delete_product.html")
    elif request.method == "POST":
                if "yes" in request.form:
                    product = Product.query.filter_by(id = product_id).first()
                    db.session.delete(product)
                    db.session.commit()
                    return redirect(url_for("dashboard"))
                else:
                    return redirect(url_for("dashboard"))
    return redirect("/")


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if "cart" not in session:
        # Initialize an empty cart and store it in the session
        session["cart"] = json.dumps(dict())
    
    cart = json.loads(session["cart"])
    
    user = current_user
    
    if request.method == "GET":
        products = [
            [Product.query.filter_by(id=product_id).first(), cart[product_id]]
            for product_id in cart.keys()
        ]
        total = sum(
            [
                int(Product.query.filter_by(id=product_id).first().price)
                * int(cart[product_id])
                for product_id in cart.keys()
            ]
        )
        return render_template("cart.html", products=products, total=total)
    
    elif request.method == "POST":
        if "remove" in request.form:
            remove_id = request.form["remove"]
            cart.pop(remove_id, None)  # Remove the item from the cart
            session["cart"] = json.dumps(cart)  # Update the session cart
            return redirect("/cart")

        # Rest of the checkout logic
        total_amount = sum(
            [
                int(Product.query.filter_by(id=product_id).first().price)
                * int(cart[product_id])
                for product_id in cart.keys()
            ]
        )
        # Create a Purchase record for each product in the cart
        for product_id, quantity in cart.items():
            product = Product.query.get(product_id)
            if int(quantity) <= product.stock:
                purchase = Purchase(
                    product=product_id,
                    customer=user.id,
                    count=int(quantity)
                   
                )
                product.stock -= int(quantity)
                db.session.add(purchase)
                db.session.commit()

        # Clear the cart after checkout
        session.pop("cart", None)
        flash("Checkout successful. Thank you for your purchase!", "sucess")
        return redirect("/")


def generate_section_graph(section):
    plt.figure(figsize=(10, 6))
    items = Product.query.filter_by(section_id=section.id).all()
    item_data = []

    for item in items:
        total_sales = Purchase.query.filter_by(product=item.id).count()
        item_data.append({
            'item_name': item.name,
            'total_sales': total_sales
        })

    item_names = [item['item_name'] for item in item_data]
    total_sales = [item['total_sales'] for item in item_data]
    plt.bar(item_names, total_sales)
    plt.title(f'Total Sales for Items in {section.name}')
    plt.xlabel('Item Name')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    graph_path = f'./static/{section.name}_graph.png'
    plt.savefig(graph_path)
    plt.close()

@app.route('/summary')
def summary():
    # Fetch data for the summary page
    sections = Section.query.all()
    section_data = []
    
    for section in sections:
        generate_section_graph(section)
        items = Product.query.filter_by(section_id=section.id).all()
        item_data = []
        
        for item in items:
            total_sales = Purchase.query.filter_by(product=item.id).count()
            item_data.append({
                'item_name': item.name,
                'item_count': item.stock,
                'total_sales': total_sales
            })

        section_data.append({
            'section_name': section.name,
            'items': item_data,
            'graph_path':  f'/{section.name}_graph.png'  # Update graph_path in the section dictionary
        })
            
    return render_template('summary.html', sections=section_data)



@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query', '').strip()
    user=current_user
    sections_with_products = Section.query.options(db.joinedload(Section.products)).all()
    search_results = []

    if query:
        # Search in products
        products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
        for product in products:
            search_results.append({
                'type': 'product',
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'stock': product.stock,
                'price': product.price
            })

        # Search in categories/sections
        sections = Section.query.filter(Section.name.ilike(f'%{query}%')).all()
        for section in sections:
             search_results.append({
        #         'type': 'section',
                'id': section.id,
                'name': section.name,
                'description': section.description
             })

    return render_template("home.html", search_results=search_results, user=user, signed=bool(user),  sections_with_products=sections_with_products,products=products)
# Add routes for product details and section details

