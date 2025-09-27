import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from extensions import db
from models import User, Role, UserRoles, Section, Product, Sale, SaleItem
from werkzeug.security import generate_password_hash
import uuid
from flask_security.utils import hash_password
from app import app
from faker_food import FoodProvider

with app.app_context():
    fake = Faker()
    fake.add_provider(FoodProvider)
    roles = ["manager", "customer"]
    # --- Sections ---
    sections = []
    for _ in range(5):  # 5 sections
        section = Section(name=fake.word().title())
        db.session.add(section)
        sections.append(section)
    db.session.commit()

    # --- Users ---
    users = []
    for _ in range(50):  # 50 users
        user = User(
            name=fake.name(),
            email=fake.unique.email(),
            password=hash_password("password123"),
            fs_uniquifier=str(uuid.uuid4()),
            active=True
        )
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Assign random roles to users
    for user in users:
        assigned_roles = random.sample([2,3], k=random.randint(0, 1))
        for role in assigned_roles:
            user.roles.append(Role.query.get(role))
    db.session.commit()

    # --- Products ---
    products = []
    price_types = ["kg", "litre"]
    for section in sections:
        for _ in range(10):  # 10 products per section
            mfd = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.utc)
            expiry = mfd + timedelta(days=random.randint(30, 365))
            product = Product(
                name=fake.fruit(),
                price=round(random.uniform(10, 1000), 2),
                in_stock=random.choice([True, True, True, False]),  # mostly in stock
                price_type=random.choice(price_types),
                mfd=mfd,
                expiry=expiry,
                section=section
            )
            db.session.add(product)
            products.append(product)
    db.session.commit()

    # --- Sales ---
    sales = []
    for _ in range(100):  # 100 sales
        customer = random.choice(users)
        sale_date = fake.date_time_between(start_date='-6mo', end_date='now', tzinfo=timezone.utc)
        sale = Sale(customer_id=customer.id, date=sale_date)
        db.session.add(sale)
        sales.append(sale)
    db.session.commit()

    # --- SaleItems ---
    for sale in sales:
        items_count = random.randint(1, 5)  # 1-5 items per sale
        sale_products = random.sample(products, k=items_count)
        for product in sale_products:
            quantity = round(random.uniform(0.5, 5.0), 2)
            item = SaleItem(
                product_id=product.id,
                quantity=quantity,
                price_at_sale=product.price,
                sale_id=sale.id
            )
            db.session.add(item)
    db.session.commit()

    print("Database seeded successfully!")
