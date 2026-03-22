from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from masters.models import Party, Company, Item
from transactions.models import SaleMaster, PurchaseMaster, Receipt, Payment
from django.db.models import Q

@login_required(login_url='login')
def global_search(request):
    query = request.GET.get('q', '').strip()
    
    results = {
        'query': query,
        'parties': [],
        'companies': [],
        'items': [],
        'sales': [],
        'purchases': [],
        'receipts': [],
        'payments': [],
        'total_results': 0
    }
    
    if query:
        # Search Parties
        results['parties'] = Party.objects.filter(
            Q(partyname__icontains=query) | 
            Q(city__icontains=query) | 
            Q(mobile__icontains=query)
        )
        
        # Search Companies (Acting as Brokers/Manufacturers)
        results['companies'] = Company.objects.filter(
            Q(companyname__icontains=query)
        )

        # Search Items
        results['items'] = Item.objects.filter(
            Q(itemname__icontains=query) |
            Q(category__categoryname__icontains=query) |
            Q(company__companyname__icontains=query)
        )
        
        # Search Sales
        results['sales'] = SaleMaster.objects.filter(
            Q(invno__icontains=query) | 
            Q(partyname__icontains=query)
        )
        
        # Search Purchases
        results['purchases'] = PurchaseMaster.objects.filter(
            Q(invno__icontains=query) | 
            Q(partyname__icontains=query)
        )
        
        # Search Receipts
        results['receipts'] = Receipt.objects.filter(
            Q(entry_no__icontains=query) | 
            Q(party_name__icontains=query)
        )
        
        # Search Payments
        results['payments'] = Payment.objects.filter(
            Q(entry_no__icontains=query) | 
            Q(party_name__icontains=query)
        )
        
        results['total_results'] = (
            results['parties'].count() + 
            results['companies'].count() + 
            results['items'].count() +
            results['sales'].count() + 
            results['purchases'].count() + 
            results['receipts'].count() + 
            results['payments'].count()
        )
        
    return render(request, 'search/global_search_results.html', results)
