from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.

@login_required
def dashboard(request):
    try:
        return render(request,
            'account/dashboard.html',
            {'section': 'dashboard'})
    except Exception as e:
        return HttpResponse("Error: {}".format(str(e)), status=500)