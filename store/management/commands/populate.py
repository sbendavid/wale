import csv
import random
import decimal
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from django.utils.text import slugify

from basket.models import Basket
from customer.models import Customer
from orders.models import OrderItem, Order
from store.models import Product, Category

class Command(BaseCommand):
    help = 'Load data into the tables'

    def handle(self, *args, **options):

        fake = Faker()

        Basket.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
        print("tables dropped successfully")

        for i in range(10):
            first_name = fake.first_name(),
            first_name = str(first_name[0])
            last_name = fake.last_name(),
            last_name = str(last_name[0])
            username = first_name + last_name,
            username = username[0]
            user = User.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = fake.ascii_free_email(), 
                password = 'Password@1'
                )
            customer = Customer.objects.get(user = user)
            customer.address = fake.address(),
            customer.address = str(customer.address[0])
            customer.save()

        categories = []
        for i in range(5):
            category_name = fake.word()
            category_slug = slugify(category_name)
            if Category.objects.filter(slug=category_slug).exists():
                category_slug = slugify(category_name)
            category = Category.objects.create(
                name=category_name,
                slug=category_slug
            )
            categories.append(category)

        csv_file_path = 'data/googleplaystore.csv'
        with open(csv_file_path, newline='', encoding="utf8") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
                product_name = row[0]
                product_slug = slugify(product_name)
                if Product.objects.filter(slug=product_slug).exists():
                    product_slug = slugify(product_name)

                products = Product.objects.create(
                    name=product_name,
                    slug=product_slug,
                    price=int(decimal.Decimal(random.randrange(155, 899)) / 10),
                    category=random.choice(categories)
                )

        products = list(Product.objects.all())
        for i in range(10):
            random_id = random.randint(0, len(products) - 1)
            basket = Basket.objects.create(
                product=products[random_id],
                quantity=random.randrange(1, 4),
            )
            basket.save()

        customers = list(Customer.objects.all())
        for customer in customers:
            order = Order.objects.create(
                customer=customer,
            )
            order_items = Basket.objects.filter()
            for basket_item in order_items:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=basket_item.product,
                    quantity=basket_item.quantity,
                    price=basket_item.product.price * basket_item.quantity
                )
                order_item.save()
            order.save()

        o_order = Order.objects.first()
        o_product = Product.objects.first()
        o_order_item = OrderItem(
            order=o_order,
            product=o_product,
            quantity=random.randrange(1, 4),
            price=o_product.price * random.randrange(1, 4)
        )
        o_order_item.save()

        print("Data loaded successfully")
