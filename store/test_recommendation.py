from unittest.mock import patch, MagicMock
from django.test import TestCase
from store.models import Product, Category
from store.recommendation_system import recommend_related_products

class TestRecommendationSystem(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Default Category")
        self.product1 = Product.objects.create(name="Product 1", price=10.0, category=self.category)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, category=self.category)
        self.product3 = Product.objects.create(name="Product 3", price=30.0, category=self.category)

    @patch("store.recommendation_system.OrderItem.objects.filter")
    def test_recommend_related_products_basic(self, mock_filter):
        mock_order_item = MagicMock()
        mock_order_item.order.orderitem_set.exclude.return_value = [self.product2]
        mock_filter.return_value = [mock_order_item]

        related = recommend_related_products(self.product1.id)
        self.assertIn(self.product2, related)
        self.assertNotIn(self.product1, related)

    @patch("store.recommendation_system.OrderItem.objects.filter")
    def test_recommend_related_products_no_orders(self, mock_filter):
        mock_filter.return_value = []
        related = recommend_related_products(self.product3.id)
        self.assertEqual(list(related), [])

    @patch("store.recommendation_system.OrderItem.objects.filter")
    def test_recommend_related_products_top_n(self, mock_filter):
        mock_order_item = MagicMock()
        mock_order_item.order.orderitem_set.exclude.return_value = [self.product2, self.product3]
        mock_filter.return_value = [mock_order_item]

        related = recommend_related_products(self.product1.id, top_n=1)
        self.assertEqual(len(related), 1)