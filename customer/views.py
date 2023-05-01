from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.

@login_required
def customer_list(request):
    try:
        user = request.user
        if user.is_authenticated and user.is_staff:
            users = User.objects.all()
            return render(request, 'customer/customer_list.html', {'users' : users})
        else:
            return redirect('account:login')
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@login_required
def customer_detail(request, id):
    try:
        user = get_object_or_404(User, id=id)
        return render(request, 'customer/customer_detail.html', {'user' : user})
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)