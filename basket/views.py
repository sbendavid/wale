from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from store.models import Product
from .basket import Basket
from .forms import BasketAddProductForm


def basket_detail(request):
    try:
        basket = Basket(request)
        for item in basket:
            item['update_quantity_form'] = BasketAddProductForm(
                initial={'quantity': item['quantity'], 'update': True})
            
        return render(request, 'basket/basket_detail.html', {'basket': basket})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@require_POST
def basket_add(request, product_id):
    try:
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        form = BasketAddProductForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            basket.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        
        return redirect('basket:basket_detail')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@require_POST
def basket_remove(request, product_id):
    try:
        basket = Basket(request)
        product = get_object_or_404(Product, id=product_id)
        basket.remove(product)
        
        return redirect('basket:basket_detail')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
