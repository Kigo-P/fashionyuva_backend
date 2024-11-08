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
    user_role = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # a relationship that maps the user to the orders
    orders = db.relationship(
        "Order", back_populates="user", cascade="all, delete-orphan"
    )
    # a relationship that maps the user to the carts
    carts = db.relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    # a relationship that maps the user to the carts
    reviews = db.relationship("Review", back_populates="user", cascade="all, delete-orphan")
    # a relationship that maps the user to the address
    address = db.relationship("Address", back_populates="user", cascade="all, delete-orphan")

    serialize_rules = (
        "-orders.user",
        "-password",
        "-carts.user",
        "-address.user",
    )

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
    quantity = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the image_id
    image_id = db.Column(db.Integer, db.ForeignKey("images.id"))
    # Foreign key from the category_id
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    # a relationship that maps the product to the images
    images = db.relationship("Image", back_populates="product")
    # a relationship that maps the product to the categories
    categories = db.relationship("Category", back_populates="product")
    # a relationship that maps the product to the orders
    orders = db.relationship(
        "Order", back_populates="product", cascade="all, delete-orphan"
    )
    # a relationship that maps the product to the carts
    carts = db.relationship(
        "Cart", back_populates="product", cascade="all, delete-orphan"
    )
    # a relationship that maps the product to the reviews
    reviews = db.relationship(
        "Review", back_populates="product", cascade="all, delete-orphan"
    )

    serialize_rules = (
        "-images.product",
        "-categories.product",
        "-orders.product",
        "-reviews.product",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<Product {self.id}: {self.title}, {self.description}, {self.price}, {self.size} has been created>"


# creating a model called Image with the table name of images
class Image(db.Model, SerializerMixin):
    __tablename__ = "images"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(), nullable=False)

    # a relationship that maps the images to the products
    product = db.relationship("Product", back_populates="images")

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
    quantity = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(), nullable=False)
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
    

    serialize_rules = (
        "-product.orders",
        "-user.orders",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<Order {self.id}: {self.total_price} , {self.quantity}, {self.status}has been created>"

# creating a model called Cart with the table name of carts
class Cart(db.Model, SerializerMixin):
    __tablename__ = "carts"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Integer(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Foreign key from the product_id
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # a relationship that maps the carts to the user
    user = db.relationship("User", back_populates="carts")
    # a relationship that maps the carts to the product
    product = db.relationship("Product", back_populates="carts")

    serialize_rules = (
        "-product.carts",
        "-user.carts",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<Cart {self.id}: {self.total_price} , {self.quantity}, {self.status}has been created>"

# creating a model called Review with the table name of reviews
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    rating= db.Column(db.String(), nullable=False)
    comment = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Foreign key from the product_id
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))

    # a relationship that maps the carts to the user
    user = db.relationship("User", back_populates="reviews")
    # a relationship that maps the carts to the product
    product = db.relationship("Product", back_populates="reviews")

    #  creating a string version using repr
    def __repr__(self):
        return f"<Review {self.id}: {self.rating} , {self.comment} has been created>"
    
# creating a model called Address with the table name of addresses
class Address(db.Model, SerializerMixin):
    __tablename__ = "addresses"

    # creating columns
    id = db.Column(db.Integer, primary_key=True)
    address= db.Column(db.String(), nullable=False)
    county= db.Column(db.String(), nullable=False)
    town= db.Column(db.String(), nullable=False)
    zip_code = db.Column(db.Integer(), nullable=False)
    country= db.Column(db.String(), nullable=False)
    # Foreign key from the user_id
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # a relationship that maps the address to the user
    user = db.relationship("User", back_populates="address")

    serialize_rules = (
        "-user.address",
    )

    #  creating a string version using repr
    def __repr__(self):
        return f"<Address {self.id}: {self.address} , {self.county} {self.town} {self.country} has been created>"
