import razorpay
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Table_detail,Table_booking,Payment_table


def reservation_form(request):
    u = request.user
    if request.method == 'POST':
        request.session['name'] = request.POST['name']
        request.session['email'] = request.POST['email']
        request.session['phone'] = request.POST['phone']
        request.session['date'] = request.POST['date']
        request.session['time_slot'] = request.POST['time_slot']

        return redirect('booking:table_booking_slot')

    return render(request, 'table_booking_form.html', {'user': u})

def table_booking(request):
    table=Table_detail.objects.all()
    u=request.user
    name = request.session.get('name')
    email = request.session.get('email')
    phone = request.session.get('phone')
    date = request.session.get('date')
    time = request.session.get('time_slot')

    booked_tables = Table_booking.objects.filter(date=date, time=time).values_list('table__table_name', flat=True)

    if(request.method=='POST'):
        s_tables=request.POST.get('selected_tables', '').split(',')
        total=len(s_tables)*200*100

        client = razorpay.Client(auth=('rzp_test_exAlWd6fwlr3BO', 'GZTfRsKfRon1EDgYk3L54sEf'))
        payment_response = client.order.create(dict(amount=total, currency='INR'))
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if (order_status == 'created'):
            p = Payment_table.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()

            tb = Table_booking.objects.create(name=name, email=email, phone=phone, date=date, time=time, user=u,booking_id=order_id)

            for table_name in s_tables:
                table_instance = Table_detail.objects.filter(table_name=table_name).first()
                if table_instance:
                    tb.table.add(table_instance)
            tb.save()
        payment_response['name'] = u.username
        return render(request,'table_payment.html',
                      {'payment':payment_response})

    return render(request,'table_booking_slot.html',{'tables':table,'booked_tables':booked_tables})
@csrf_exempt
def payment_status(request,u):
    if not request.user.is_authenticated:
        u = User.objects.get(username=u)
        login(request, u)


    if(request.method=='POST'):
        response=request.POST
        print(response)
        print(u)
        param_dict={'razorpay_payment_id':response['razorpay_payment_id'],
                    'razorpay_order_id':response['razorpay_order_id'],
                    'razorpay_signature':response['razorpay_signature']
                    }
        client = razorpay.Client(auth=('rzp_test_exAlWd6fwlr3BO', 'GZTfRsKfRon1EDgYk3L54sEf'))

        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)

            order = Payment_table.objects.get(order_id=response['razorpay_order_id'])
            order.razorpay_payment_id = response['razorpay_payment_id']
            order.paid = True
            order.save()

            user = User.objects.get(username=u)
            tb = Table_booking.objects.filter(user=user, booking_id=response['razorpay_order_id'])
            print('booked',tb)

            for i in tb:
                i.payment_status = "paid"
                for table_instance in i.table.all():  
                    table_instance.booking_status = "confirm"
                    table_instance.save()
                i.save()
        except:
            pass

    return render(request,'payment_status.html')

