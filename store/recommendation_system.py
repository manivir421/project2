
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


from .models import Product, OrderItem

def recommend_related_products(product_id, top_n=5):
    # Get all OrderItems for the given product
    order_items = OrderItem.objects.filter(product_id=product_id)

    # Collect all other products bought in the same orders
    related_products = []
    for item in order_items:
        other_items = item.order.orderitem_set.exclude(product_id=product_id)
        for other in other_items:
            related_products.append(other.product)

    # Remove duplicates while preserving order
    related_products = list(dict.fromkeys(related_products))

    return related_products[:top_n]
