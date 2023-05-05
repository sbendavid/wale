from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.urls import reverse
from .models import Category, Product
from basket.forms import BasketAddProductForm
from store.forms import SearchForm

# Create your views here.

def product_list(request, category_slug=None):
    try:
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(
                Category, 
                slug=category_slug)
            products = products.filter(category=category)

        context = {
            'category': category, 
            'categories': categories,
            'products': products
            }

        return render(request, 'store/product_list.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def product_detail(request, id, slug):
    try:
        product = get_object_or_404(Product, id=id, available=True)

        if slug != product.slug:
            if not slug:
                return HttpResponseRedirect(
                    reverse('product_detail', args=[product.id, product.slug]))
            else:
                return HttpResponseRedirect(
                    reverse('product_detail', args=[product.id, product.get_slug()]))
            
        basket_product_form = BasketAddProductForm()

        context = {
            'product': product, 
            'basket_product_form': basket_product_form
            }

        return render(request, 'store/product_detail.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

def product_search(request):
    try:
        search = request.GET.get('search')
        products = []

        if search:
            search_list = search.split()
            q = Q()
            for word in search_list:
                q |= Q(name__icontains=word) | Q(description__icontains=word)
            products = Product.objects.filter(q)

        form = SearchForm(initial={'search_query': search})

        context = {
            'form': form,
            'products': products,
            'search': search,
        }

        return render(request, 'store/product_search.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)