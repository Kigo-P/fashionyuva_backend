from faker import Faker
from app import app
from models import (
    db,
    User,
    Product,
    Image,
    Category,
    Order,
    OrderProduct,
    Review,
    Address,
    ContactUs,
    Payment,
    Newsletter,
)
import random
from werkzeug.security import generate_password_hash

# Initialize Faker
fake = Faker()


def seed_data():
    # Start by resetting the database
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
            contact=fake.msisdn()[:10],  # Ensure contact is 10 digits
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
            category_id=random.choice(categories).id,
        )
        db.session.add(product)
        products.append(product)
    db.session.commit()

    # Create Orders
    orders = []
    for _ in range(20):
        order = Order(
            total_price=random.randint(20, 1000),
            status=random.choice(["pending", "shipped", "delivered", "canceled"]),
            user_id=random.choice(users).id,
        )
        db.session.add(order)
        orders.append(order)
    db.session.commit()

    # Create OrderProducts
    for _ in range(30):
        order_product = OrderProduct(
            quantity=random.randint(1, 5),
            product_id=random.choice(products).id,
            order_id=random.choice(orders).id,
        )
        db.session.add(order_product)
    db.session.commit()

    # Create Reviews
    for _ in range(15):
        review = Review(
            rating=str(random.randint(1, 5)),
            comment=fake.sentence(),
            user_id=random.choice(users).id,
            product_id=random.choice(products).id,
        )
        db.session.add(review)
    db.session.commit()

    # Create Addresses
    for user in users:
        address = Address(
            address=fake.address(),
            county=fake.state(),
            town=fake.city(),
            zip_code=int(fake.zipcode()[:5]),
            country=fake.country(),
            user_id=user.id,
        )
        db.session.add(address)
    db.session.commit()

    # Create ContactUs entries
    for _ in range(5):
        contact_us = ContactUs(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            contact=fake.msisdn()[:10],  # Ensure contact is 10 digits
            about_us=fake.sentence(),
            message=fake.text(),
            users_id=random.choice(users).id,
        )
        db.session.add(contact_us)
    db.session.commit()

    # Create Payments
    for order in orders:
        payment = Payment(amount=order.total_price, order_id=order.id)
        db.session.add(payment)
    db.session.commit()

    # Create Newsletter entries
    for _ in range(5):
        newsletter = Newsletter(email=fake.unique.email())
        db.session.add(newsletter)
    db.session.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    # Use the application context
    with app.app_context():
        seed_data()
