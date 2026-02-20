from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Category, Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.models import User


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    return render(request, 'home.html', {
        'categories': categories,
        'products': products
    })


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # name = request.POST['name']
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('register')
        
        # Create user and customer
        user = User.objects.create_user(username=username, email=email, password=password)
        customer = Customer.objects.create(user=user, email=email)
        Cart.objects.create(customer=customer)
        
        # Login user
        login(request, user)
        messages.success(request, 'Account created!')
        return redirect('home')
    
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('home')

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()  

    return render(request, 'products.html', {
        'products': products,
        'categories': categories   
    })

def product_detail(request, product_id):
    categories = Category.objects.all()   
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'product_detail.html', {
        'product': product,
        'categories': categories   
    })

@login_required
def cart(request):
    customer = Customer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart__customer=customer)
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    customer = Customer.objects.get(user=request.user)
    cart = Cart.objects.get(customer=customer)
    
    # Add to cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, 'Added to cart!')
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Removed from cart')
    return redirect('cart')

@login_required
def checkout(request):
    customer = Customer.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart__customer=customer)
    
    if not cart_items:
        messages.error(request, 'Cart is empty')
        return redirect('cart')
    
    # Create order
    order = Order.objects.create(customer=customer)
    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    
    # Clear cart
    cart_items.delete()
    
    messages.success(request, 'Order placed!')
    return redirect('home')

def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    return render(request, 'products.html', {
        'products': products,
        'selected_category': category
    })
