import email
from django.shortcuts import render, redirect
from . models import *
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F
from . forms import CheckOutForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from .utils import isFirebaseAuthenticated, id_generator
from . decorators import isAuthenticated

def store(request):
    user = isFirebaseAuthenticated(request.session.get('uid'))
    products = Product.objects.order_by('-name')
    categories = Product.category_list
    cartItems = 0
    if user:
        try:
            order = Order.objects.get(
                customer__email=user['email'], complete=False)
            cartItems = order.get_cart_items
        except:
            cartItems = 0
    else:
        pass

    page_num = request.GET.get('page', 1)
    paginator = Paginator(products, 8)

    try:
        page = paginator.page(page_num)
    except:
        page = paginator.page(1)

    context = {
        'products': page,
        'categories': categories,
        'pages': page,
        'cartTotal': cartItems
    }
    return render(request, 'store/index.html', context)


def product(request, pk):
    user = isFirebaseAuthenticated(request.session.get('uid'))
    if user:
        customer = Customer.objects.get(email=user['email'])

    product = Product.objects.get(pk=pk)
    featured_products = Product.objects.filter(category=product.category)
    try:
        cartItems = Order.objects.get(
            customer=customer, complete=False).get_cart_items
    except:
        cartItems = 0
    context = {
        'product': product,
        'featured': featured_products[:3],
        'cartTotal': cartItems
    }

    return render(request, 'store/product.html', context)


@isAuthenticated
def add_to_cart(request, pk):
    user = isFirebaseAuthenticated(request.session.get('uid'))
    if user:
        if request.method == "POST":
            customer = Customer.objects.get(email=user['email'])
            product = Product.objects.get(pk=pk)
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            orderItem, created = OrderItem.objects.get_or_create(
                product=product, order=order)
            orderItem.quantity = F('quantity') + request.POST.get('quantity')
            orderItem.save()
            cartTotal = order.get_cart_items
        else:
            return redirect('store')

    return JsonResponse(cartTotal, safe=False)


@isAuthenticated
def cart(request):
    user = isFirebaseAuthenticated(request.session.get('uid'))
    customer = Customer.objects.get(email=user['email'])
    try:
        order = Order.objects.get(customer=customer, complete=False)
        cartItems = order.get_cart_items
        total_amount = order.get_cart_total
        orderItem = OrderItem.objects.filter(order=order)
    except Exception as e:
        print(e)
        cartItems = 0
        total_amount = 0
        orderItem = {}

    context = {
        'cartTotal': cartItems,
        'total_amount': total_amount,
        'products': orderItem

    }
    return render(request, 'store/cart.html', context)


@isAuthenticated
def update_cart(request, pk):
    if request.method == 'POST':
        user = isFirebaseAuthenticated(request.session.get('uid'))
        customer = Customer.objects.get(email=user['email'])
        order = Order.objects.get(customer=customer, complete=False)
        orderItem, create = OrderItem.objects.get_or_create(
            product__id=pk, order=order)
        action = request.POST.get('action')
        quantity = request.POST.get('quantity')
        if(action == 'add'):
            orderItem.quantity = F('quantity') + quantity
        elif(action == 'remove'):
            orderItem.quantity = F('quantity') - quantity
        elif(action == 'delete'):
            orderItem.quantity = 0

        orderItem.save()
        orderItem.refresh_from_db()

        cartItems = order.get_cart_items
        cartTotal = order.get_cart_total

        qty = orderItem.quantity
        if qty <= 0:
            orderItem.delete()
    else:
        raise PermissionDenied

    data = {
        'cartItems': cartItems,
        'orderQty': qty,
        'cartTotal': cartTotal
    }

    return JsonResponse([cartItems, qty, cartTotal], safe=False)


@isAuthenticated
def checkout(request):
    form = CheckOutForm()
    user = isFirebaseAuthenticated(request.session.get('uid'))
    if user:
        customer = Customer.objects.get(email=user['email'])
        try:
            order = Order.objects.get(customer=customer, complete=False)
            cartItems = order.get_cart_items
            total_amount = order.get_cart_total
            orderItem = OrderItem.objects.filter(order=order)
        except:
            cartItems = 0
            total_amount = 0
            orderItem = {}

    context = {
        'cartTotal': cartItems,
        'total_amount': total_amount,
        'orders': orderItem,
        'form': form

    }
    return render(request, 'store/checkout.html', context)


def process_order(request):
    if request.method == "POST":
        user = isFirebaseAuthenticated(request.session.get('uid'))
        if user:
            customer = Customer.objects.get(email=user['email'])
            order = Order.objects.get(customer=customer, complete=False)
        form = CheckOutForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.order = order
            instance.customer = customer
            order.complete = True
            order.transaction_id = order.id + 100000
            order.save()
            instance.save()
            print('saved!')
        else:
            return JsonResponse('Error saving', safe=False)

    return redirect('store')


@isAuthenticated
def track_order(request):
    orders = {}
    order = 0
    cartTotal = 0
    user = isFirebaseAuthenticated(request.session.get('uid'))
    if user:
        try:
            customer = Customer.objects.get(email=user['email'])
            orders = Order.objects.filter(
                customer=customer, complete=True).order_by('-date_ordered')
            order = Order.objects.get(customer=customer, complete=False)
            cartTotal = order.get_cart_items
        except:
            pass

    page_num = request.GET.get('page', 1)
    paginator = Paginator(orders, 2)

    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    context = {
        'orders': page,
        'cartTotal': cartTotal,
        'pages': page
    }
    return render(request, 'store/track_order.html', context)
