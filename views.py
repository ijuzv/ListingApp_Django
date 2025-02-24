from django.shortcuts import render, redirect
from django.urls import reverse
from products.models import Vehicle, VehicleImage, CustomUser
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
import json

# Home Page
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        profile = request.FILES.get('profile')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered')
        elif CustomUser.objects.filter(contact=contact).exists():
            messages.error(request, 'Contact number is already in use')
        else:
            user = CustomUser(
                username = username,
                profile = profile,
                contact = contact,
                email = email,
                address = address,
                user_type = user_type,
                password = make_password(password)
            )
            user.save()
            
            messages.success(request, 'Registration successful! Please log in')
            return redirect('login')
    return render(request, 'register.html')
    
# User Login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
         
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found')
                
    return render(request, 'login.html')
    

# User Logout
def logout_view(request):
    logout(request)
    return redirect("home")

def products(request):
    product_list = Vehicle.objects.all()  # Fetch all products
    return render(request, 'products.html', {'products': product_list})

def product_detail(request, pk):
    product = get_object_or_404(Vehicle, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def post(request):
    if request.method == "POST":

        # Get data from the form
        product_type = request.POST.get('product_type')
        brand = request.POST.get('brand')
        model_year = request.POST.get('model_year')
        fuel_type = request.POST.get('fuel_type')
        km_driven = request.POST.get('km_driven')
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        owners = request.POST.get('owners')
        insurance = request.POST.get('insurance') == 'on'
        images = request.FILES.getlist('images')

        vehicle = Vehicle.objects.create(
            product_type=product_type,
            brand=brand,
            model_year=model_year,
            fuel_type=fuel_type,
            km_driven=km_driven,
            title=title,
            description=description,
            price=price,
            owners=owners,
            insurance=insurance,
        )

        for image in images:
            VehicleImage.objects.create(
                vehicle=vehicle,
                image=image
            )

        return redirect(reverse('product_detail', kwargs={'pk': vehicle.pk}))

    years = range(2000, 2025)
    return render(request, 'post.html', {'years': years})


def about(request):
    pass

def contact(request):
    pass