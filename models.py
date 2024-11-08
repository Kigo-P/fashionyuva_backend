from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy

#  initializing metadata and adding it to the db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)

# creating a model called User with the table name of users
class User(db.model, SerializerMixin):
    __tablename__ = "users"

    # creating columns
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(), nullable = False)
    last_name = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    user_role = db.Column(db.String(), nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # a relationship that maps the user to the orders
    orders = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")

    #  creating a string version using repr
    def __repr__(self):
        return f"<User {self.id}: {self.first_name}, {self.last_name}, {self.email}, {self.user_role} has been created>"

# creating a model called Product with the table name of products
class Product(db.model, SerializerMixin):
    __tablename__ = "products"

    # creating columns
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(), nullable = False)
    description = db.Column(db.String(), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    size = db.Column(db.String(), nullable = False)
    color = db.Column(db.String(), nullable = False)
    material = db.Column(db.String(), nullable = False)
    quantity = db.Column(db.Integer(), nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the image_id
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    # Foreign key from the category_id
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    # a relationship that maps the product to the images
    images = db.relationship("Image", back_populates="product", cascade="all, delete-orphan")
    # a relationship that maps the product to the categories
    categories = db.relationship("Category", back_populates="product", cascade="all, delete-orphan")
    # a relationship that maps the product to the orders
    orders = db.relationship("Order", back_populates="product", cascade="all, delete-orphan")

    #  creating a string version using repr
    def __repr__(self):
        return f"<Product {self.id}: {self.title}, {self.description}, {self.price}, {self.size} has been created>"

# creating a model called Image with the table name of images
class Image(db.model, SerializerMixin):
    __tablename__ = "images"

    # creating columns
    id = db.Column(db.Integer, primary_key = True)
    url = db.Column(db.String(), nullable = False)

    # a relationship that maps the images to the products
    product = db.relationship("Product", back_populates="images")

    #  creating a string version using repr
    def __repr__(self):
        return f"<Image {self.id}: {self.url} has been created>"
    
# creating a model called Category with the table name of categories
class Category(db.model, SerializerMixin):
    __tablename__ = "categories"

    # creating columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), nullable = False)

    # a relationship that maps the categories to the products
    product = db.relationship("Product", back_populates="categories")

    #  creating a string version using repr
    def __repr__(self):
        return f"<Category {self.id}: {self.name} has been created>"

# creating a model called Order with the table name of orders
class Order(db.model, SerializerMixin):
    __tablename__ = "orders"

    # creating columns
    id = db.Column(db.Integer, primary_key = True)
    total_price = db.Column(db.Integer(), nullable = False)
    quantity = db.Column(db.Integer(), nullable = False)
    status = db.Column(db.String(), nullable = False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Foreign key from the product_id
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))


    # a relationship that maps the orders to the user
    user = db.relationship("User", back_populates="orders")
    # a relationship that maps the orders to the products
    product = db.relationship("Product", back_populates="orders")


