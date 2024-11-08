from faker import Faker
from app import app
from models import db, User, Product, Image, Category, Order
import random
from werkzeug.security import generate_password_hash

# Initialize Faker
fake = Faker()


def seed_data():
    # Start by resetting the database (delete all data in a controlled way)
    db.drop_all()
    db.create_all()

    # Create Categories
    categories = []
    for _ in range(5):
        category = Category(name=fake.word().capitalize())
        db.session.add(category)
        categories.append(category)
    db.session.commit()

    # Create Images
    images = []
    for _ in range(10):
        image = Image(url=fake.image_url())
        db.session.add(image)
        images.append(image)
    db.session.commit()

    # Create Users
    users = []
    for _ in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            password=generate_password_hash("password"),
            user_role=random.choice(["customer", "admin"]),
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Create Products
    products = []
    for _ in range(15):
        product = Product(
            title=fake.word().capitalize(),
            description=fake.text(max_nb_chars=100),
            price=random.randint(10, 500),
            size=random.choice(["S", "M", "L", "XL"]),
            color=random.choice(["red", "blue", "green", "yellow", "black"]),
            material=random.choice(["cotton", "wool", "silk"]),
            quantity=random.randint(1, 50),
            image_id=random.choice(images).id,
            category_id=random.choice(categories).id,
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()

    # Create Orders
    for _ in range(20):
        order = Order(
            total_price=random.randint(20, 1000),
            quantity=random.randint(1, 5),
            status=random.choice(["pending", "shipped", "delivered", "canceled"]),
            user_id=random.choice(users).id,
            product_id=random.choice(products).id,
        )
        db.session.add(order)
    db.session.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    # Use the application context
    with app.app_context():
        seed_data()
