from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods
from django.db.models import Sum

from masters.models import Party
from transactions.models import SaleMaster, PurchaseMaster, Receipt, Payment

# Create your views here.

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    context = {}
    context["total_parties"] = Party.objects.count()
    context["total_sales"] = SaleMaster.objects.count()
    context["total_purchases"] = PurchaseMaster.objects.count()
    
    context["total_sale_amount"] = SaleMaster.objects.aggregate(total=Sum("net_amount"))["total"] or 0
    context["total_purchase_amount"] = PurchaseMaster.objects.aggregate(total=Sum("net_amount"))["total"] or 0
    
    total_receipts = Receipt.objects.aggregate(total=Sum("amount"))["total"] or 0
    total_payments = Payment.objects.aggregate(total=Sum("amount"))["total"] or 0
    context["total_balance"] = total_receipts - total_payments

    return render(request, 'core/home.html', context)

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'auth/login.html')

@never_cache
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
