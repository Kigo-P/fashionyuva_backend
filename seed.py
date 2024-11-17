from random import choice as rc
from faker import Faker
from werkzeug.security import generate_password_hash
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
from datetime import datetime

# Initialize Faker
fake = Faker()

# Define constants
USER_ROLES = ["customer", "admin"]
CATEGORIES = ["Men", "Women", "Children"]
ORDER_STATUSES = ["ordered", "pending", "canceled"]
COLORS = ["red", "blue", "green", "yellow", "black"]
MATERIALS = ["cotton", "wool", "silk"]
SIZES = ["S", "M", "L", "XL"]

with app.app_context():
    # Reset and recreate the database
    db.drop_all()
    db.create_all()

    # Create User instances
    users = [
        User(
            first_name="Alice",
            last_name="Johnson",
            email="alice@gmail.com",
            password=generate_password_hash("12345"),
            contact="0720114113",
            user_role="admin",
        ),
        User(
            first_name="Bob",
            last_name="Smith",
            email="bob@gmail.com",
            password=generate_password_hash("12345"),
            contact="0798012234",
            user_role="customer",
        ),
        User(
            first_name="Eve",
            last_name="Davis",
            email="eve@gmail.com",
            password=generate_password_hash("12345"),
            contact="0721134890",
            user_role="customer",
        ),
    ]

    db.session.add_all(users)
    db.session.commit()

    categories = [
        Category(name="Men", description="Apparel and accessories tailored for men."),
        Category(
            name="Women", description="A wide range of products curated for women."
        ),
        Category(
            name="Children", description="Quality and safe products for children."
        ),
    ]

    db.session.add_all(categories)
    db.session.commit()
    # Define products with 10 items
    products = [
        Product(
            title="Classic Denim Jacket",
            price=7500,
            description="A timeless denim jacket with a comfortable fit, perfect for layering.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="denim",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Casual Cotton T-Shirt",
            price=1500,
            description="Soft, breathable cotton tee ideal for everyday wear.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="cotton",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Elegant Silk Blouse",
            price=9500,
            description="Luxurious silk blouse with a relaxed fit for a sophisticated look.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="silk",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Woolen Winter Sweater",
            price=6000,
            description="Warm and cozy wool sweater to keep you comfortable during cold days.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="wool",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Stylish Cotton Hoodie",
            price=5000,
            description="A modern, comfortable hoodie made from premium cotton fabric.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="cotton",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Leather Boots",
            price=12000,
            description="Premium leather boots designed for comfort and durability.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="leather",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Puffer Jacket",
            price=8000,
            description="A warm and stylish puffer jacket, perfect for cold weather.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="nylon",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Summer Dress",
            price=3500,
            description="A light and breezy dress ideal for sunny weather.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="cotton",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Running Sneakers",
            price=5500,
            description="Lightweight and comfortable sneakers for your daily run.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="mesh",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
        Product(
            title="Luxury Watch",
            price=15000,
            description="A high-end watch combining style and precision.",
            size=rc(SIZES),
            color=rc(COLORS),
            material="stainless steel",
            quantity=fake.random_int(min=1, max=50),
            category_id=rc(categories).id,
        ),
    ]

    db.session.add_all(products)
    db.session.commit()

    images = [
        Image(
            url="https://images.pexels.com/photos/910599/pexels-photo-910599.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            product_id=1,
        ),
        Image(
            url="https://images.pexels.com/photos/9558567/pexels-photo-9558567.jpeg?auto=compress&cs=tinysrgb&w=600",
            product_id=2,
        ),
        Image(
            url="https://images.pexels.com/photos/7680335/pexels-photo-7680335.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1",
            product_id=3,
        ),
        Image(
            url="https://images.pexels.com/photos/10157851/pexels-photo-10157851.jpeg?auto=compress&cs=tinysrgb&w=600",
            product_id=4,
        ),
        Image(
            url="https://images.pexels.com/photos/8217308/pexels-photo-8217308.jpeg?auto=compress&cs=tinysrgb&w=600",
            product_id=5,
        ),
    ]

    db.session.add_all(images)
    db.session.commit()

    last_order = Order.query.order_by(Order.id.desc()).first()
    last_order_id = last_order.id if last_order else None
    new_order_id = 0
    if last_order_id is None:
        new_order_id = 1
    else:
        new_order_id = last_order_id + 1

    current_year = datetime.now().year
    receipt_number = f"#REC-{current_year:04d}-{new_order_id:03d}"

    orders = [
        Order(
            total_price=fake.random_int(min=20, max=1000),
            status=rc(ORDER_STATUSES),
            user_id=rc(users).id,
            receipt_no=receipt_number,
        )
        for _ in range(5)
    ]

    db.session.add_all(orders)
    db.session.commit()

    # Create OrderProduct instances
    order_products = [
        OrderProduct(
            quantity=fake.random_int(min=1, max=5),
            product_id=rc(products).id,
            order_id=rc(orders).id,
        )
        for _ in range(10)
    ]

    db.session.add_all(order_products)
    db.session.commit()

    reviews = [
        Review(
            rating=str(fake.random_int(min=1, max=5)),
            comment=fake.sentence(),
            user_id=rc(users).id,
            product_id=rc(products).id,
        )
        for _ in range(10)
    ]

    db.session.add_all(reviews)
    db.session.commit()

    addresses = [
        Address(
            address=fake.address(),
            county=fake.state(),
            town=fake.city(),
            zip_code=int(fake.zipcode()[:5]),
            country=fake.country(),
            user_id=user.id,
        )
        for user in users
    ]

    db.session.add_all(addresses)
    db.session.commit()

    # Create ContactUs instances
    contact_us_entries = [
        ContactUs(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            contact=fake.msisdn()[:10],
            about_us=fake.sentence(),
            message=fake.text(),
            users_id=rc(users).id,
        )
        for _ in range(5)
    ]

    db.session.add_all(contact_us_entries)
    db.session.commit()

    # Create Payment instances
    payments = [
        Payment(amount=order.total_price, order_id=order.id) for order in orders
    ]

    db.session.add_all(payments)
    db.session.commit()

    # Create Newsletter entries
    newsletters = [Newsletter(email=fake.unique.email()) for _ in range(5)]
    db.session.add_all(newsletters)
    db.session.commit()

    print("Database seeded successfully!")
