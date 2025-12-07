
#comp 3450 <Ashima,ripan>--> */
# shop/recommendation_system.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product, Order

# Example: Recommend products that are commonly bought with the current product
def recommend_related_products(product_id, top_n=5):
    # Get all orders where the product was bought
    orders = Order.objects.filter(product_id=product_id)

    # Get the product ids of all other products purchased in the same orders
    other_product_ids = [order.product.id for order in orders]

    # Exclude the current product from the list
    other_product_ids = [pid for pid in other_product_ids if pid != product_id]

    # Get the top N related products (this is basic collaborative filtering)
    related_products = Product.objects.filter(id__in=other_product_ids).distinct()[:top_n]

    return related_products
