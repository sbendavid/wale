import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from orders.models import Order
from store.models import Product
from .forms import LoginForm, UserRegistrationForm

# Create your views here.

@login_required
def dashboard(request):
    try:
        orders_by_month = (
            Order.objects
            .annotate(month=TruncMonth('created'))
            .values('month')
            .annotate(total_orders=Count('id'))
            .order_by('month')
        )

        products_by_month = (
            Product.objects
            .annotate(month=TruncMonth('created'))
            .values('month')
            .annotate(total_products=Count('order_items', distinct=True))
            .order_by('month')
        )

        customers_by_month = (
            Order.objects
            .annotate(month=TruncMonth('created'))
            .values('month')
            .annotate(total_customers=Count('customer', distinct=True))
            .order_by('month')
        )

        labels = [o['month'].strftime('%Y-%m') for o in orders_by_month]
        data = {
            'orders': [o['total_orders'] for o in orders_by_month],
            'products': [p['total_products'] for p in products_by_month],
            'customers': [c['total_customers'] for c in customers_by_month],
        }

        chart_data = {'labels': labels, 'data': data}

        return render(request, 'account/dashboard.html', {'chart_data': json.dumps(chart_data)})

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('store:product_list')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('store:product_list')


def sign_up(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/sign_up_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/sign_up.html', {'user_form': user_form})