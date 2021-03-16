from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm


def home(request):
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    total_order = orders.count()
    
    total_customers = customers.count()
    
    context = {'products': products, 'customers': customers, 'orders': orders,
               'total_customers': total_customers, 'total_order': total_order,
               'delivered': delivered, 'pending': pending}
    # return HttpResponse("This is home page")
    return render(request, "accounts/dashboard.html", context)


def product(request):
    products = Product.objects.all()
    return render(request, "accounts/products.html", {'products': products})


def customer(request, pk):
    customer1 = Customer.objects.get(id=pk)
    orders = customer1.order_set.all()
    context = {'customer': customer1, 'orders': orders}
    return render(request, "accounts/customer.html", context)


def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, "accounts/order_form.html", context)


def createOrders(request, pk):
    customer1 = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer1})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, "accounts/order_form.html", context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form': form, 'order': order}
    return render(request, "accounts/order_form.html", context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    
    if request.method == 'POST':
        order.delete()
        return redirect("/")
    
    context = {
        'form': form,
        'order': order,
    }
    return render(request, "accounts/delete_order.html", context)
