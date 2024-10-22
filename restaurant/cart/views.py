from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from shop.models import Dish
import razorpay

from .models import Cart, Payment_table, Order_table
from booking.models import Table_booking


@login_required
def view_cart(request):
    u = request.user
    cart = Cart.objects.filter(user=u)
    total = 0
    for i in cart:
        total = total + i.quantity * i.dish.price
    return render(request, 'view_cart.html', {'cart': cart, 'total': total})


@login_required
def add_to_cart(request, id):
    d = Dish.objects.get(id=id)
    u = request.user
    try:
        c = Cart.objects.get(user=u, dish=d)
        c.quantity += 1
        c.save()

    except:
        c = Cart.objects.create(user=u, dish=d, quantity=1)
        c.save()
    return redirect('cart:view_cart')


@login_required
def decrement(request, id):
    u = request.user
    d = Dish.objects.get(id=id)
    try:
        c = Cart.objects.get(user=u, dish=d)
        if (c.quantity == 1):
            c.delete()
        else:
            c.quantity -= 1
            c.save()
    except:
        pass

    return redirect('cart:view_cart')


@login_required
def remove_cart(request, id):
    u = request.user
    d = Dish.objects.get(id=id)

    try:
        c = Cart.objects.get(user=u, dish=d)
        c.delete()
    except:
        pass

    return redirect('cart:view_cart')


@login_required
def orderform(request):
    if (request.method == 'POST'):
        phone = request.POST['ph']
        address = request.POST['ad']
        pin = request.POST['pin']
        u = request.user

        c = Cart.objects.filter(user=u)

        total = 0
        for i in c:
            total = total + (i.quantity * i.dish.price)
        total = int(total * 100)

        client = razorpay.Client(auth=('rzp_test_exAlWd6fwlr3BO', 'GZTfRsKfRon1EDgYk3L54sEf'))
        payment_response = client.order.create(dict(amount=total, currency='INR'))
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if (order_status == 'created'):
            p = Payment_table.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()
            for i in c:
                o = Order_table.objects.create(user=u, dish=i.dish, address=address, phone=phone, pin=pin,
                                               no_of_items=i.quantity, order_id=order_id)
                o.save()
        payment_response['name'] = u.username
        return render(request, 'payment.html', {'payment': payment_response})
    return render(request, 'order_form.html')


@csrf_exempt
def payment_status(request, u):
    print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        u = User.objects.get(username=u)
        login(request, u)
        print(request.user.is_authenticated)

    if (request.method == 'POST'):
        response = request.POST
        print(response)
        print(u)
        param_dict = {'razorpay_payment_id': response['razorpay_payment_id'],
                      'razorpay_order_id': response['razorpay_order_id'],
                      'razorpay_signature': response['razorpay_signature']
                      }
        client = razorpay.Client(auth=('rzp_test_exAlWd6fwlr3BO', 'GZTfRsKfRon1EDgYk3L54sEf'))

        try:
            status = client.utility.verify_payment_signature(param_dict)
            print(status)

            order = Payment_table.objects.get(order_id=response['razorpay_order_id'])
            order.razorpay_payment_id = response['razorpay_payment_id']
            order.paid = True
            order.save()

            user = User.objects.get(username=u)
            cart = Cart.objects.filter(user=user)
            o = Order_table.objects.filter(user=user, order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status = "paid"
                i.save()
            cart.delete()

        except:
            pass

    return render(request, 'payment_status.html')


def my_orders(request):
    user = request.user
    order = Order_table.objects.filter(user=user, payment_status='paid')
    print('orders',order)
    booking = Table_booking.objects.filter(user=user, payment_status='paid')
    print('tables',booking)
    return render(request, 'my_orders.html', {'orders': order,'bookings':booking})
