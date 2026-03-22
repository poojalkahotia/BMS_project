from django.shortcuts import render, redirect
from .models import Party, Item, Company, Category
from .forms import PartyForm, ItemForm, CompanyForm, CategoryForm

def party_create(request):
    if request.method == 'POST':
        form = PartyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('party_list')
    else:
        form = PartyForm()
    return render(request, 'masters/party_form.html', {'form': form})

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

def party_delete(request, pk):
    party = Party.objects.get(pk=pk)
    if request.method == 'POST':
        party.delete()
        return redirect('party_list')
    return render(request, 'masters/party_confirm_delete.html', {'party': party})

def party_list(request):
    parties = Party.objects.all().order_by('partyname')
    return render(request, 'masters/party_list.html', {'parties': parties})

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'masters/item_form.html', {'form': form})

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

def item_delete(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'masters/item_confirm_delete.html', {'item': item})

def item_list(request):
    items = Item.objects.all().order_by('itemname')
    return render(request, 'masters/item_list.html', {'items': items})

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

from django.http import JsonResponse

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

def get_item_details(request):
    item_name = request.GET.get('item_name')
    try:
        item = Item.objects.get(itemname=item_name)
        data = {
            'rate': item.sale_rate
        }
    except Item.DoesNotExist:
        data = {'rate': 0}
    return JsonResponse(data)
