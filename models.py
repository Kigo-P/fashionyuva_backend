from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

#  initializing metadata and adding it to the db
metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


# creating a model called User with the table name of users
class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    contact = db.Column(db.String(), nullable=False)
    user_role = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # a relationship that maps the user to the orders
    orders = db.relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )

    # a relationship that maps the user to the carts
    reviews = db.relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )
    # a relationship that maps the user to the address
    address = db.relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )
    # a relationship that maps the user to the contactus
    contactus = db.relationship(
        "ContactUs", back_populates="user", cascade="all, delete-orphan"
    )

    serialize_rules = (
        "-orders.user",
        "-password",
        "-address.user",
        "-contactus.user",
        "-reviews.user",
    )
    

    # validating the email
    @validates("email")
    def validate_email(self, key, address):
        if "@" not in address:
            raise ValueError("Failed simple email validation")
        return address

    # validating users contact to be exactly 10 digits
    @validates("contact")
    def validates_contact(self, key, value):
        if not value or len(value) != 10 or not value.isdigit():
            raise ValueError("The contact must have 10 digits")
        else:
            return value

    #  creating a string version using repr
    def __repr__(self):
        return f"<User {self.id}: {self.first_name}, {self.last_name}, {self.email}, {self.user_role} has been created>"


# creating a model called Product with the table name of products
class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    color = db.Column(db.String(), nullable=False)
    material = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the category_id
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    # a relationship that maps the product to the images
    images = db.relationship("Image", back_populates="product", cascade="all, delete-orphan")
    # a relationship that maps the product to the categories
    categories = db.relationship("Category", back_populates="product")
    # a relationship that maps the product to the orderproducts
    orderproduct = db.relationship(
        "OrderProduct", back_populates="product", cascade="all, delete-orphan"
    )
    # a relationship that maps the product to the reviews
    reviews = db.relationship(
        "Review", back_populates="product", cascade="all, delete-orphan"
    )

    serialize_rules = (
        "-images.product",
        "-categories.product",
        "-orderproduct.product",
        "-reviews.product",
    )

    #  validating the price of the product to be a positive number
    @validates("price")
    def validates_price(self, key, price):
        if price < 1:
            raise ValueError("Price must be between greater than 1")
        return price

    #  creating a string version using repr
    def __repr__(self):
        return f"<Product {self.id}: {self.title}, {self.description}, {self.price}, {self.size} has been created>"


# creating a model called Image with the table name of images
class Image(db.Model, SerializerMixin):
    __tablename__ = "images"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), nullable=False)
    # Foreign key from the product_id
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # a relationship that maps the images to the products
    product = db.relationship(
        "Product", back_populates="images", single_parent=True
    )

    serialize_rules = ("-product.images",)

    #  creating a string version using repr
    def __repr__(self):
        return f"<Image {self.id}: {self.url} has been created>"


# creating a model called Category with the table name of categories
class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # a relationship that maps the categories to the products
    product = db.relationship("Product", back_populates="categories")

    serialize_rules = ("-product.categories",)

    #  creating a string version using repr
    def __repr__(self):
        return f"<Category {self.id}: {self.name} has been created>"


# creating a model called Order with the table name of orders
class Order(db.Model, SerializerMixin):
    __tablename__ = "orders"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # a relationship that maps the orders to the user
    user = db.relationship("User", back_populates="orders")
    # a relationship that maps the orders to the orderproduct
    orderproduct = db.relationship(
        "OrderProduct", back_populates="order", cascade="all, delete-orphan"
    )
    # a relationship that maps the orders to the payment
    payment = db.relationship(
        "Payment", back_populates="order", cascade="all, delete-orphan"
    )

    serialize_rules = (
        "-orderproduct.order",
        "-user.orders",
        "-payment.order",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<Order {self.id}: {self.total_price} , {self.status}has been created>"


# creating a model called OrderProducts with the table name of orderproducts
class OrderProduct(db.Model, SerializerMixin):
    __tablename__ = "orderproducts"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    # Foreign key from the product_id
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    # Foreign key from the order_id
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    # a relationship that maps the orderproducts to the product
    product = db.relationship("Product", back_populates="orderproduct")
    # a relationship that maps the orderproducts to the order
    order = db.relationship("Order", back_populates="orderproduct")

    serialize_rules = (
        "-product.orderproduct",
        "-order.orderproduct",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<OrderProduct {self.id}: {self.quantity} has been created>"


# creating a model called Review with the table name of reviews
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Foreign key from the product_id
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # a relationship that maps the reviews to the user
    user = db.relationship("User", back_populates="reviews")
    # a relationship that maps the reviews to the product
    product = db.relationship("Product", back_populates="reviews")

    serialize_rules = (
        "-user",
        "-product",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<Review {self.id}: {self.rating} , {self.comment} has been created>"


# creating a model called Address with the table name of addresses
class Address(db.Model, SerializerMixin):
    __tablename__ = "addresses"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(), nullable=False)
    county = db.Column(db.String(), nullable=False)
    town = db.Column(db.String(), nullable=False)
    zip_code = db.Column(db.Integer(), nullable=False)
    country = db.Column(db.String(), nullable=False)
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # a relationship that maps the address to the user
    user = db.relationship("User", back_populates="address")

    serialize_rules = ("-user.address",)

    #  creating a string version using repr
    def __repr__(self):
        return f"<Address {self.id}: {self.address} , {self.county} {self.town} {self.country} has been created>"


# creating ContactUs Model
class ContactUs(db.Model, SerializerMixin):
    __tablename__ = "contactus"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    contact = db.Column(db.String(), nullable=False)
    about_us = db.Column(db.String(), nullable=False)
    message = db.Column(db.String(), nullable=False)
    # Foreign key from the users id
    users_id = db.Column(db.Integer(), db.ForeignKey("users.id"))

    #  a relationship mapping the contact to the buyer
    user = db.relationship("User", back_populates="contactus")

    # setting serialization rules
    serialize_rules = ("-user.contactus",)

    # validating users contact to be exactly 10 digits
    @validates("contact")
    def validates_contact(self, key, value):
        if not value or len(value) != 10 or not value.isdigit():
            raise ValueError("The contact must have 10 digits")
        else:
            return value

    #  creating a string version using repr
    def __repr__(self):
        return f"<Contact {self.id}: {self.first_name} , {self.last_name} {self.email} {self.contact} has been created>"


# creating Payment Model
class Payment(db.Model, SerializerMixin):
    __tablename__ = "payments"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer(), nullable=False)
    # Foreign key from the order_id
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    # a relationship that maps the payment to the order
    order = db.relationship("Order", back_populates="payment")

    serialize_rules = ("-order.payment",)

    #  creating a string version using repr
    def __repr__(self):
        return f"<Payment {self.id}: {self.amount} has been created>"


# creating Newsletter Model
class Newsletter(db.Model, SerializerMixin):
    __tablename__ = "newsletter"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)

    #  creating a string version using repr
    def __repr__(self):
        return f"<Newsletter {self.id}: {self.email} has been created>"
