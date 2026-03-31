from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Party, Item, Company, Category
from .forms import PartyForm, ItemForm, CompanyForm, CategoryForm

@login_required(login_url='login')
def party_create(request):
    if request.method == 'POST':
        form = PartyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('party_list')
    else:
        form = PartyForm()
    return render(request, 'masters/party_form.html', {'form': form})

@login_required(login_url='login')
def party_update(request, pk):
    party = Party.objects.get(pk=pk)
    if request.method == 'POST':
        form = PartyForm(request.POST, instance=party)
        if form.is_valid():
            form.save()
            return redirect('party_list')
    else:
        form = PartyForm(instance=party)
    return render(request, 'masters/party_form.html', {'form': form})

@login_required(login_url='login')
def party_delete(request, pk):
    party = Party.objects.get(pk=pk)
    if request.method == 'POST':
        party.delete()
        return redirect('party_list')
    return render(request, 'masters/party_confirm_delete.html', {'party': party})

@login_required(login_url='login')
def party_list(request):
    parties = Party.objects.all().order_by('partyname')
    paginator = Paginator(parties, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'masters/party_list.html', {'parties': page_obj, 'page_obj': page_obj})

@login_required(login_url='login')
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'masters/item_form.html', {'form': form})

@login_required(login_url='login')
def item_update(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'masters/item_form.html', {'form': form})

@login_required(login_url='login')
def item_delete(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'masters/item_confirm_delete.html', {'item': item})

@login_required(login_url='login')
def item_list(request):
    items = Item.objects.all().order_by('itemname')
    paginator = Paginator(items, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'masters/item_list.html', {'items': page_obj, 'page_obj': page_obj})

@login_required(login_url='login')
def company_create(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('company_create')
    else:
        form = CompanyForm()
    companies = Company.objects.all().order_by('companyname')
    return render(request, 'masters/company_form.html', {'form': form, 'companies': companies})

@login_required(login_url='login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_create')
    else:
        form = CategoryForm()
    categories = Category.objects.all().order_by('categoryname')
    return render(request, 'masters/category_form.html', {'form': form, 'categories': categories})

@login_required(login_url='login')
def company_delete(request, pk):
    if request.method == 'POST':
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        messages.success(request, 'Company deleted successfully!')
    return redirect('company_create')

@login_required(login_url='login')
def category_delete(request, pk):
    if request.method == 'POST':
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('category_create')

from django.http import JsonResponse

@login_required(login_url='login')
def get_party_details(request):
    party_name = request.GET.get('party_name')
    try:
        party = Party.objects.get(partyname=party_name)
        data = {
            'add1': party.add1,
            'add2': party.add2,
            'city': party.city,
            'mobile': party.mobile,
            'email': party.email
        }
    except Party.DoesNotExist:
        data = {}
    return JsonResponse(data)

@login_required(login_url='login')
def get_item_details(request):
    item_name = request.GET.get('item_name')
    try:
        item = Item.objects.get(itemname=item_name)
        data = {
            'rate': item.sale_rate,
            'sale_rate': item.sale_rate,
            'purchase_rate': item.purchase_rate
        }
    except Item.DoesNotExist:
        data = {'rate': 0, 'sale_rate': 0, 'purchase_rate': 0}
    return JsonResponse(data)
