
#comp 3450 <Ashima,ripan>--> */
from django.contrib import admin
from .models import Coupon , ReviewRating


from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

class CouponAdmin(admin.ModelAdmin):  # Corrected spelling of admin
    list_display = ['code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']

admin.site.register(Coupon, CouponAdmin)

admin.site.register(ReviewRating)
 
 