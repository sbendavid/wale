from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import OrderItem, Order
from .forms import OrderCreateForm
from basket.basket import Basket

# Create your views here.

def order_create(request):
    try:
        basket = Basket(request)
        if request.method == 'POST':
            form = OrderCreateForm(request.POST)
            if form.is_valid():
                order = form.save()
                for item in basket:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity'])
                basket.clear()
            return render(request, 'orders/created.html', {'order': order})
        else:
            form = OrderCreateForm()

        context = {
            'basket': basket, 
            'form': form
            }

        return render(request, 'orders/create.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
    
def order_list(request):
    try:
        orders = Order.objects.all()

        return render(request, 'orders/order_list.html', {'orders' : orders})
    
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def order_detail(request, id):
    try:
        order = get_object_or_404(Order, id=id)
        customer = order.customer
        user = get_object_or_404(User, id=customer.pk)
        order_items = OrderItem.objects.filter(order_id=order.id)

        context = {
            'order' : order, 
            'user': user, 
            'order_items': order_items
            }

        return render(request, 'orders/order_detail.html', context)
    
    except Exception as e:
            return HttpResponse(f"Error: {str(e)}", status=500)