
#comp 3450 <Ashima,ripan>--> */
from django.urls import path
from . import views
from .views import cart, calculate_total_after_discount
from .views import product_list
from .views import camera_view
from .views import dashboard 
from .views import community_index
from .views import geolocation_view
from .views import product_detail, virtual_try_on
from django.conf import settings
from django.conf.urls.static import static
from .views import filter_products
from .views import transaction_history
from .views import contact_view, contact_success_view
from .views import return_view
from .views import exchange_view  # Import your exchange view
from .views import help

from django.urls import path
from .views import virtual_lipstick_view


from django.urls import path
from .views import voice_chat
from django.urls import include, path

from django.urls import path
from .views import ar, verify_face



urlpatterns = [
    path('', views.store, name='store'),
    
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('transaction-history/', transaction_history, name='transaction_history'),
    path('help/', help, name='help'),
    path('exchange/', exchange_view, name='exchange'),
    path('return/', return_view, name='return.html'),
    path('virtual-room/', views.virtual_room_view, name='virtual_room'),
    path('contact/', contact_view, name='contact'),
    path('contact/success/', contact_success_view, name='contact_success'),
    path('searchproduct/', views.searchproduct, name="searchproduct"),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    path('camera/', camera_view, name='camera_view'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
    path('product-list/', product_list, name='product_list'),
    path('lobby/', views.lobby , name="lobby"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', community_index, name='community_index'),
    path('geolocation/', geolocation_view, name='geolocation'),
    path('filter-products/', filter_products, name='filter_products'),
    path('voice_chatbot/', views.voice_chat, name='voice_chatbot'),
    path('ar/', views.ar, name='ar'),  # URL to access AR page
   # path('ar/', ar, name='ar'),
    path('verify/', verify_face, name='verify_face'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('virtual-try-on/<int:product_id>/', virtual_try_on, name='virtual_try_on'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
    path('calculate_total_after_discount/', calculate_total_after_discount, name='calculate_total_after_discount'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('lipstick/', virtual_lipstick_view, name='virtual_lipstick'),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

