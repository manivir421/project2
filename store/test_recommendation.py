import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")
django.setup()

from django.test import TestCase
from store.models import Product, Order, OrderItem, Category, Customer
from store.recommendation_system import recommend_related_products

class TestRecommendationSystem(TestCase):

    def setUp(self):
        # Create a default category
        self.category = Category.objects.create(name="Default Category")
        # Create a test customer
        self.customer = Customer.objects.create(name="Test User", email="test@test.com", phone_no="1234567890")

        # Create products
        self.product1 = Product.objects.create(name="Product 1", price=10.0, category=self.category)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, category=self.category)
        self.product3 = Product.objects.create(name="Product 3", price=30.0, category=self.category)

        # Create an order
        self.order = Order.objects.create(customer=self.customer, complete=True)

        # Link products to order using OrderItem
        OrderItem.objects.create(order=self.order, product=self.product1, quantity=1)
        OrderItem.objects.create(order=self.order, product=self.product2, quantity=1)

    def test_recommend_related_products_basic(self):
        related = recommend_related_products(self.product1.id)
        self.assertIn(self.product2, related)
        self.assertNotIn(self.product1, related)

    def test_recommend_related_products_no_orders(self):
        related = recommend_related_products(self.product3.id)
        self.assertEqual(list(related), [])

    def test_recommend_related_products_top_n(self):
        related = recommend_related_products(self.product1.id, top_n=1)
        self.assertEqual(len(related), 1)