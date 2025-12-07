import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")
django.setup()


from django.test import TestCase
from store.models import Product, Order
from store.recommendation_system import recommend_related_products

class TestRecommendationSystem(TestCase):

    def setUp(self):

        self.product1 = Product.objects.create(name="Product 1")
        self.product2 = Product.objects.create(name="Product 2")
        self.product3 = Product.objects.create(name="Product 3")

  
        Order.objects.create(product=self.product1)
        Order.objects.create(product=self.product2)


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
