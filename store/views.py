
#comp 3450 <Ashima,ripan>--> */
from .forms import UserRegistrationForm
from django.shortcuts import render, redirect,get_object_or_404
from .models import *
from django.urls import reverse
from django.http import JsonResponse
import json
from .forms import CustomerForm
from datetime import datetime
from .utils import cookieCart , cartData
from .utils import guestOrder
from django.contrib.auth import login,authenticate
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect  # Add this line
from django.contrib.auth import login, authenticate, logout
from .models import Product, Category
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import WishlistItem, Product,VirtualTryOn
from .models import Coupon, Product , ReviewRating
from django.shortcuts import render, redirect
from .models import Coupon,Order
from .forms import ReviewForm
from django.contrib.auth.models import User
from .models import Topic
import cv2
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import DiscussionMessage
from .forms import DiscussionMessageForm
from opencage.geocoder import OpenCageGeocode
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import PriceFilterForm
from django.template.loader import render_to_string
from .models import Product, ProductAttribute
from django.db.models import Min, Max
from .models import ContactMessage
from django.core.mail import send_mail
from .forms import ContactForm


from django.http import HttpResponse
import cv2
import mediapipe as mp
import numpy as np
from django.http import JsonResponse





import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render, get_object_or_404
from .models import Product, Order
from .recommendation_system import recommend_related_products
from .models import SearchHistory


import random
import os
import base64
import cv2
import numpy as np
import json

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render




# Create your views here.



from django.shortcuts import render
from .models import Product, Category, SearchHistory
from .utils import cartData

def store(request):
    # Fetch all products and categories
    products = Product.objects.all()
    categories = Category.objects.all()

    # Fetch cart data
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    # Initialize an empty list for recommended products
    recommended_products = []

    if request.user.is_authenticated:
        # Get the last 5 searches of the user
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')[:5]
        
        # Fetch products related to the search queries
        for history in search_history:
            related_products = Product.objects.filter(title__icontains=history.search_query)
            recommended_products.extend(related_products)

        # Remove duplicate products by converting to a set and back to a list
        recommended_products = list(set(recommended_products))

    context = {
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
        'order': order,
        'items': items,
        'recommended_products': recommended_products,  # Add the recommended products here
        'shipping': False  # Existing context variable
    }

    return render(request, 'store/store.html', context)

def category_list(request,category_slug):
    categories=Category.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={'products':products,'categories':categories,'category':category,'shipping':False}
    return render(request,'store/category_list.html',context)


def product_detail(request, slug):
    categories = Category.objects.all()
    products = Product.objects.all()
    product = get_object_or_404(Product, slug=slug)
    product_reviews = ReviewRating.objects.filter(product=product)
    try_on_images = VirtualTryOn.objects.filter(product=product)
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    


    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Process the form and save the review
            # ...

            messages.success(request, 'Review submitted successfully.')
            return redirect('product_detail', product_id=product_id)
    else:
        form = ReviewForm()


    context = {'product': product, 'categories': categories, 'shipping': False, 'product_reviews': product_reviews,'try_on_images': try_on_images,
        'form': form,}

    customer_info = None
    if product_reviews.exists():
        customer_info = product_reviews.first().user

    context['customer_info'] = customer_info
    return render(request, 'store/product_detail.html', context)

    
      
 
def cart(request):
    products=Product.objects.all()
    categories = Category.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    coupon_code = request.GET.get('coupon_code')

    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
                order.coupon = coupon
                order.save()
                messages.success(request, 'Coupon applied successfully.')
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.')

    context = {'items': items, 'categories': categories, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)



    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0,'get_cart_total':0}
        cartItems=order['get_cart_items'] 

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def checkout(request):
    categories=Category.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'categories': categories, 'order': order, 'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


    

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
 
    return JsonResponse('Items was added ',safe=False)


from django.views.decorators.csrf import csrf_exempt
import datetime
@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    print(transaction_id)
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
         customer, order = guestOrder(request, data)   
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
    
    return JsonResponse("Payment Complete ", safe=False)

def signup_view(request):
    
    categories=Category.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            

            messages.success(request, 'You have successfully signed up!')
            return redirect('login')  # Redirect to the customer's profile or any other page you want
        else:
            # Display form errors as messages
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f'{user_form.fields[field].label}: {error}')

            for field, errors in customer_form.errors.items():
                for error in errors:
                    messages.error(request, f'{customer_form.fields[field].label}: {error}')
    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerForm()
    
    context={'items':items,'categories':categories,'order':order,'cartItems':cartItems,'shipping':'False','user_form': user_form, 'customer_form': customer_form}    

    return render(request, 'store/signup.html',context)
def login_view(request):
    
    categories=Category.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('store')  # Redirect to the customer's profile or any other page you want
            else:
                form.add_error(None, "Invalid username or password.")
                messages.error(request, 'Login failed. Please check your credentials and try again.')
    else:
        form = LoginForm()
        
    context={'form': form,'items':items,'categories':categories,'order':order,'cartItems':cartItems,'shipping':'False'}
    return render(request, 'store/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('store') 

def productlistAjax(request):
    products = Product.objects.filter(is_active=True).values_list('title', flat=True)
    productList = list(products)

    return JsonResponse(productList, safe=False)

from django.urls import reverse

from django.shortcuts import redirect
from django.urls import reverse
from .models import Product, Category
from django.contrib import messages

def searchproduct(request):
    if request.method == "POST":
        searched_term = request.POST.get('productsearch')

        if searched_term == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:

            
            product = Product.objects.filter(title__icontains=searched_term).first()

            if product:
                
                url = reverse('product_detail', kwargs={'slug': product.slug})
                return redirect(url)
            else:
                messages.info(request,"No product matched your search")
               # return redirect(request.META.get('HTTP_REFERER'))
            
            

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def wishlist(request):
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # Check if the item is already in the wishlist
    if WishlistItem.objects.filter(user=user, product=product).exists():
        # You might want to handle the case where the item is already in the wishlist
        # For now, let's just redirect back to the product detail page
        return redirect(product.get_absolute_url())

    # If the item is not in the wishlist, add it
    WishlistItem.objects.create(user=user, product=product)

    return redirect(product.get_absolute_url())
@login_required
def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')
def calculate_total_after_discount(request):
    coupon_code = request.GET.get('coupon_code')
    
    if not coupon_code:
        return JsonResponse({'error': 'Coupon code is missing'}, status=400)

    # Assuming you have a way to determine the current user, replace this with your actual logic
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        # If the user is not authenticated, handle the case appropriately (e.g., create a guest order)
        # Replace the following line with your actual guest order creation logic
        customer, order = None, None

    try:
        coupon = Coupon.objects.get(code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
        order.coupon = coupon
        order.save()
        total_after_discount = calculate_total_with_discount(coupon_code)
        return JsonResponse({'total_after_discount': total_after_discount})
    except Coupon.DoesNotExist:
        return JsonResponse({'error': 'Invalid coupon code'}, status=400)


def add_review(request, product_id):
    if request.method == 'POST':
        # Process the form data and save the review
        # For example, assuming you have a Review model with 'text' and 'rating' fields
        text = request.POST['text']
        rating = request.POST['rating']
        product = Product.objects.get(pk=product_id)

        review = Review.objects.create(
            product=product,
            text=text,
            rating=rating,
            # Add other fields as needed
        )

        messages.success(request, 'Review added successfully.')
        return redirect('product_detail', product_id=product_id)
    else:
        # Handle GET request (display the form for adding a review)
        # You can render a template with a form for users to submit reviews
        return render(request, 'store/add_review.html')  # Replace with the actual template name


def submit_review(request, product_id):
    
    if request.method == "POST":
        url = request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted")
                return redirect(url)

def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:3]
    min_price = ProductAttribute.objects.aggregate(min_price=Min('price'))
    max_price = ProductAttribute.objects.aggregate(Max('price'))

    return render(request, 'store/product_list.html', {
    'data': data,
    'total_data': total_data,
    'min_price': min_price['min_price'],
    'max_price': max_price,
})
def lobby(request):
    return render(request, 'lobby.html')

def camera_view(request):
    return render(request, 'camera.html')

@receiver(post_save, sender=Product)
def check_out_of_stock(sender, instance, **kwargs):
    if instance.quantity == 0 and not instance.is_out_of_stock:
        instance.is_out_of_stock = True
        instance.save()

        # Notify users
        subject = f"{instance.name} is out of stock"
        message = f"{instance.name} is now out of stock. Please check the website for updates."
        
        # Replace with your own email address
        from_email = 'ashimabhasin489@gmail.com'

@receiver(post_save, sender=Product)
def check_product_availability(sender, instance, **kwargs):
    if instance.quantity > 0 and instance.is_out_of_stock:
        instance.is_out_of_stock = False
        instance.save()

        # Notify users
        subject = f"{instance.name} is back in stock"
        message = f"{instance.name} is now back in stock. Place your order now!"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email for user in instance.notified_users.all()])

def subscribe_to_notifications(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        product.notified_users.add(request.user)
        product.save()
        # Optionally, you can send a confirmation message to the user.
    return redirect('product_detail', product_id=product_id)
        

@login_required
def dashboard(request):
    user = request.user
    # Add any additional context data you want to pass to the template
    context = {'user': user}
    return render(request, 'accounts/dashboard.html', context)

def community_index(request):
    messages = DiscussionMessage.objects.all().order_by('-created_at')

    if request.method == 'POST':
        discussion_form = DiscussionMessageForm(request.POST)
        if discussion_form.is_valid():
            discussion_form.save()
            # Redirect to avoid form resubmission on page refresh
            return redirect('store:community_index')
    else:
        discussion_form = DiscussionMessageForm()

    return render(request, 'store/index.html', {'discussion_form': discussion_form, 'messages': messages})

def geolocation_view(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        # Replace 'YOUR_OPENCAGE_API_KEY' with your actual OpenCage API key
        api_key = 'fb1880bba269446ca222c83d9907f2d5'

        geocoder = OpenCageGeocode(api_key)
        result = geocoder.reverse_geocode(latitude, longitude)

        # Extract the formatted address from the result
        if result and len(result):
            formatted_address = result[0]['formatted']
        else:
            formatted_address = 'Location not found'

        return render(request, 'store/geolocation.html', {'formatted_address': formatted_address})

    return render(request, 'store/geolocation.html')
def virtual_try_on(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST' and 'user_image' in request.FILES:
        user_image = request.FILES['user_image']

        # Process the virtual try-on and save the result
        try_on_image = process_try_on(product, user_image)

        # Save the try-on image in the database
        VirtualTryOn.objects.create(product=product, try_on_image=try_on_image)

        messages.success(request, 'Virtual Try-On successful.')
        return redirect('product_detail', product_id=product_id)

    context = {
        'product': product,
    }
    return render(request, 'store/virtual_try_on.html', context)

def process_try_on(product, user_image):
    # Create a unique filename for the try-on image
    try_on_image_name = f'try_on_results/{product.id}_{user_image.name}'

    # Save the try-on image to the media root using FileSystemStorage
    fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
    try_on_image = fs.save(try_on_image_name, user_image)

    return try_on_image

def filter_products(request):
    allProducts = Product.objects.all()

    # Get the minimum price
    min_price = ProductAttribute.objects.aggregate(Min('price'))['price__min']

    # Get the price parameter from the request
    price_param = request.GET.get('price')

    # Check if price_param is not None and is a valid integer
    if price_param is not None and price_param.isdigit():
        price_param = int(price_param)
        
        # Filter only if min_price is not None
        if min_price is not None:
            allProducts = allProducts.filter(productattribute__price__gte=min_price)

    return render(request, 'store/product_list.html', {'allProducts': allProducts, 'min_price': min_price})

def transaction_history(request):
    transactions = [
        {'date': '2023-11-23', 'description': 'Elegant White padded top', 'amount': '15.00'},
        {'date': '2023-11-24', 'description': 'Baby Kajal', 'amount': '$15.00'},
        {'date': '2023-11-25', 'description': 'Baby Towel', 'amount': '$10.00'},
        # Add more transactions as needed
    ]

    return render(request, 'store/transaction_history.html', {'transactions': transactions})


    

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'store/contact_form.html', {'form': form})

def contact_success_view(request):
    return render(request, 'store/contact_success.html')

from django.shortcuts import render

def virtual_room_view(request):
    # Your view logic goes here
    return render(request, 'store/virtual_room.html')

from django.shortcuts import render

def return_view(request):
    # Your view logic here
    return render(request, 'store/return.html')

def exchange_view(request):
    # Your view logic here
    return render(request, 'store/exchange.html')

def help(request):
    # Your view logic here
    return render(request, 'store/help.html')





from django.http import JsonResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # For testing. Remove when handling CSRF properly.
def voice_chat(request):
    if request.method == "GET":
        # Render the chatbot page when visited via GET
        return render(request, 'store/voice_chatbot.html')

    elif request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            user_input = data.get("text", "").strip()
            
            if not user_input:
                return JsonResponse({"response": "I didn't catch that. Please try again."})
            
            # Generate a simple response (you can integrate with AI later)
            response_text = get_response(user_input)
            return JsonResponse({"response": response_text})
        except Exception as e:
            return JsonResponse({"response": "Error: " + str(e)}, status=400)
    
    return JsonResponse({"response": "Invalid request method."}, status=405)

def get_response(user_input):
    # Basic responses for demonstration purposes.
    responses = {
        "hello": "Hi there! How can I help you today?",
        "how are you": "I'm good, thanks for asking. How can I assist you?",
        "bye": "Goodbye! Have a great day!",
        "i am feeling sad today":" sad, i am there to help you anytime, my love",
    }
    
    lower_text = user_input.lower()
    for key, value in responses.items():
        if key in lower_text:
            return value
    return f"You said: '{user_input}'. I'm still learning to understand you!"

from django.shortcuts import render
"""
def ar(request):
    return render(request, 'store/ar.html')  # Render the AR page template

"""
def virtual_lipstick_view(request):
    # Your code here. 
    # Possibly capture from webcam or just return a response?
    main()
    return HttpResponse("Hello from the Virtual Lipstick view!")


# shop/views.py

""""
def product_detail(request, product_id):
    # Get the product being viewed
    product = get_object_or_404(Product, id=product_id)
    
    # Get the recommended products (those commonly bought with the current product)
    recommended_products = recommend_related_products(product_id)

    # Render the product detail page with recommendations
    return render(request, 'product_detail.html', {
        'product': product,
        'recommended_products': recommended_products
    })
"""



# Define paths for the Haar Cascade and known faces
CASCADE_PATH = os.path.join(settings.BASE_DIR, "haarcascade_frontalface_default.xml")
KNOWN_FACES_DIR = os.path.join(settings.BASE_DIR, "static", "known_faces")

# Global LBPH face recognizer and mapping of label to user name.
recognizer = None
label_to_name = {}

def train_recognizer():
    """
    Train the LBPH face recognizer using images stored in KNOWN_FACES_DIR.
    Each image file's name (without extension) is treated as the user's name.
    For now, this function is a placeholder—replace with your actual training code.
    """
    global recognizer, label_to_name

    # Here you would typically:
    #   1. Initialize the recognizer:
    #       recognizer = cv2.face.LBPHFaceRecognizer_create()
    #   2. Loop through images in KNOWN_FACES_DIR, read them in grayscale,
    #      and add them along with a numeric label.
    #   3. Train the recognizer using recognizer.train(faces, np.array(labels))
    #
    # For now, we'll leave it as a placeholder.
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces = []
    labels = []
    current_label = 0

    if not os.path.isdir(KNOWN_FACES_DIR):
        print("KNOWN_FACES_DIR not found. Skipping training.")
        return

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(KNOWN_FACES_DIR, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            faces.append(img)
            labels.append(current_label)
            # Use the filename (without extension) as the user's name.
            label_to_name[current_label] = os.path.splitext(filename)[0]
            current_label += 1

    if len(faces) == 0:
        print("No training images found in KNOWN_FACES_DIR.")
        return

    recognizer.train(faces, np.array(labels))
    print("Recognizer trained on {} image(s).".format(len(faces)))

# Train the recognizer at startup.
train_recognizer()

def ar(request):
    """
    Renders the ar.html template.
    Make sure ar.html exists in your templates folder.
    """
    return render(request, "store/ar.html")

@csrf_exempt
def verify_face(request):
    """
    Receives a POST request with a base64-encoded image.
    Detects a face and uses the LBPH recognizer to determine whether the face is known or new.
    Returns a JSON response with the result.
    """
    if request.method == "POST":
        try:
            if recognizer is None:
                return JsonResponse({"message": "Recognizer not initialized."}, status=400)

            data = json.loads(request.body)
            img_base64 = data.get("image")
            if not img_base64:
                return JsonResponse({"message": "No image data received."}, status=400)

            # Remove the data URL prefix.
            try:
                _, encoded = img_base64.split(",", 1)
            except Exception as split_error:
                raise Exception("Failed to split the base64 image string: " + str(split_error))
            img_bytes = base64.b64decode(encoded)

            # Convert the image bytes to a NumPy array and decode to an image.
            np_arr = np.frombuffer(img_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            if frame is None:
                raise Exception("Could not decode image from provided data.")

            # Convert to grayscale for detection and recognition.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Load Haar Cascade for face detection.
            face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
            if face_cascade.empty():
                raise Exception("Haar Cascade XML file not found or failed to load at " + CASCADE_PATH)
            
            # Detect faces using Haar Cascade.
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            if len(faces) == 0:
                return JsonResponse({"message": "No face detected. Please try again."})

            # Process only the first detected face.
            (x, y, w, h) = faces[0]
            roi_gray = gray[y:y+h, x:x+w]

            # Recognize the face.
            label_id, confidence = recognizer.predict(roi_gray)
            threshold = 80.0  # Adjust threshold as needed.

            if confidence < threshold:
                user_name = label_to_name.get(label_id, "Unknown")
                response_data = {"message": f"Welcome back, {user_name}."}
            else:
                response_data = {"message": "Face not recognized. Please register."}

            return JsonResponse(response_data)
        except Exception as e:
            print("Error processing image:", str(e))
            return JsonResponse({"message": f"Error processing image: {str(e)}"}, status=500)

    return JsonResponse({"message": "Invalid request method."}, status=400)