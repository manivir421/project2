import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")  
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User  
from store.models import Product, Order, Category  
from store.recommendation_system import recommend_related_products

class TestRecommendationSystem(TestCase):

    def setUp(self):
   
        self.category = Category.objects.create(name="Default Category")

 
        self.product1 = Product.objects.create(
            name="Product 1", price=10.0, category=self.category
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=20.0, category=self.category
        )
        self.product3 = Product.objects.create(
            name="Product 3", price=30.0, category=self.category
        )

       
        self.user = User.objects.create(username="testuser")

        Order.objects.create(product=self.product1, user=self.user)   
        Order.objects.create(product=self.product2, user=self.user)   

 

    def test_recommend_related_products_basic(self):
        #Test that related products are recommended correctly.
        related = recommend_related_products(self.product1.id)
        self.assertIn(self.product2, related)
        self.assertNotIn(self.product1, related)

    def test_recommend_related_products_no_orders(self):
        #Test a product with no orders returns empty recommendations.
        related = recommend_related_products(self.product3.id)
        self.assertEqual(list(related), [])

    def test_recommend_related_products_top_n(self):
        #Test that top_n parameter limits the number of recommendations.
        related = recommend_related_products(self.product1.id, top_n=1)
        self.assertEqual(len(related), 1)