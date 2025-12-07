#/*<!---
#comp 3450 <Ashima,ripan>--> */
from django.views.decorators.http import require_POST
from django import forms
from django.contrib.auth.models import User
from .models import Customer
from django import forms
from .models import ReviewRating
from .models import DiscussionMessage
from .models import ContactMessage


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_no']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon=Coupon.objects.get(code__iexact=code,
            valid_from__lte=now,
            valid_to__gte=now,
            active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = coupon.id
    return redirect('cart:cart_detail')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'rating', 'review']

class DiscussionMessageForm(forms.ModelForm):
    class Meta:
        model = DiscussionMessage
        fields = ['user', 'message']

class PriceFilterForm(forms.Form):
    color = forms.CharField(max_length=50, required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'subject', 'message']