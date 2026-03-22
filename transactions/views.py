from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import SaleMaster, SaleDetail, PurchaseMaster, PurchaseDetail, Receipt, Payment
from masters.models import Party, Item
import json
from datetime import datetime

# --- SALE VIEWS ---

def sale_entry(request, pk=None):
    parties = Party.objects.all().order_by('partyname')
    items = Item.objects.all().order_by('itemname')
    
    sale_data = None
    sale = None
    
    if pk:
        sale = get_object_or_404(SaleMaster, pk=pk)
        next_inv = sale.invno
        
        # Construct data dictionary for JS
        sale_data = {
            'isEditing': True,
            'partyName': sale.partyname,
            'partyDetails': {
                'add1': sale.add1 or '',
                'add2': sale.add2 or '',
                'city': sale.city or '',
                'mobile': sale.mobile or '',
                'email': sale.email or ''
            },
            'items': [
                {
                    'item': detail.itemname.itemname,
                    'qty': float(detail.qty),
                    'rate': float(detail.rate),
                    'amount': float(detail.itemamt)
                } for detail in sale.details.all()
            ]
        }
        sale_data = json.dumps(sale_data) # Serialize to JSON string
    else:
        # Generate next Invoice Number (Simple logic: Count + 1)
        last_inv = SaleMaster.objects.all().count()
        next_inv = f"INV-{last_inv + 1:04d}"
    
    return render(request, 'transactions/sale_entry.html', {
        'parties': parties,
        'items': items,
        'next_inv': next_inv,
        'sale': sale,
        'sale_data': sale_data # Pass JSON string
    })

@csrf_exempt
def save_sale(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                party = Party.objects.get(partyname=data['party_name'])
                
                # Determine inv_no
                if data['inv_no'] == 'New':
                    last_inv_count = SaleMaster.objects.all().count()
                    final_inv_no = f"INV-{last_inv_count + 1:04d}"
                    is_update = False
                else:
                    final_inv_no = data['inv_no']
                    # Check if exists to determine update vs create with specific ID
                    is_update = SaleMaster.objects.filter(pk=final_inv_no).exists()

                # Update or Create SaleMaster
                sale_master, created = SaleMaster.objects.update_or_create(
                    invno=final_inv_no,
                    defaults={
                        'invdate': data['inv_date'],
                        'party': party,
                        'partyname': data['party_name'],
                        'add1': data.get('add1'),
                        'add2': data.get('add2'),
                        'city': data.get('city'),
                        'mobile': data.get('mobile'),
                        'email': data.get('email', ''),
                        'total': data['sub_total'],
                        'discount_per': data['discount_per'],
                        'discount_amt': data['discount_amt'],
                        'adjustment': data['adjustment'],
                        'net_amount': data['net_amount'],
                        'amount_in_words': data['amount_in_words'],
                        'remark': data['remark']
                    }
                )
                
                # Handle Details: Delete existing if updating to replace with new set
                if not created:
                    sale_master.details.all().delete()

                # Create SaleDetails
                items_data = data['items']
                for item_row in items_data:
                    item_obj = Item.objects.get(itemname=item_row['item_name'])
                    SaleDetail.objects.create(
                        invno=sale_master,
                        itemname=item_obj,
                        qty=item_row['qty'],
                        rate=item_row['rate'],
                        itemamt=item_row['amount'],
                        itemremark='' 
                    )
            
            msg = 'Sale Updated Successfully!' if is_update else 'Sale Saved Successfully!'
            return JsonResponse({'status': 'success', 'message': msg})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

def sale_list(request):
    sort = request.GET.get("sort", "-invdate")
    direction = request.GET.get("direction", "desc")
    
    order = sort if direction == "asc" else f"-{sort}"
    # Default sorting is complex because of original code having '-invdate', '-invno'
    # Fallback to secondary if needed, or stick to simple sorting as requested.
    if sort == "-invdate":
        order = "-invdate" # default
    
    sales = SaleMaster.objects.all().order_by(order, '-invno').prefetch_related('details__itemname')
    return render(request, 'transactions/sale_list.html', {
        'sales': sales,
        'current_sort': sort,
        'current_direction': direction
    })

# --- PURCHASE VIEWS ---

def purchase_edit(request, pk):
    return purchase_entry(request, pk=pk)

def purchase_entry(request, pk=None):
    parties = Party.objects.all().order_by('partyname')
    items = Item.objects.all().order_by('itemname')
    
    purchase_data = None
    purchase = None
    
    if pk:
        purchase = get_object_or_404(PurchaseMaster, pk=pk)
        next_inv = purchase.invno
        
        # Construct data dictionary for JS
        purchase_data = {
            'isEditing': True,
            'partyName': purchase.partyname,
            'partyDetails': {
                'add1': purchase.add1 or '',
                'add2': purchase.add2 or '',
                'city': purchase.city or '',
                'mobile': purchase.mobile or '',
                'email': purchase.email or ''
            },
            'items': [
                {
                    'item': detail.itemname.itemname,
                    'qty': float(detail.qty),
                    'rate': float(detail.rate),
                    'amount': float(detail.itemamt)
                } for detail in purchase.details.all()
            ]
        }
        purchase_data = json.dumps(purchase_data)
    else:
        # Generate next Invoice Number (Simple logic: Count + 1)
        last_inv = PurchaseMaster.objects.all().count()
        next_inv = f"PUR-{last_inv + 1:04d}"
    
    return render(request, 'transactions/purchase_entry.html', {
        'parties': parties,
        'items': items,
        'next_inv': next_inv,
        'purchase': purchase,
        'purchase_data': purchase_data
    })

@csrf_exempt
def save_purchase(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            with transaction.atomic():
                party = Party.objects.get(partyname=data['party_name'])
                
                # Determine inv_no
                if data['inv_no'] == 'New':
                    last_inv_count = PurchaseMaster.objects.all().count()
                    final_inv_no = f"PUR-{last_inv_count + 1:04d}"
                    is_update = False
                else:
                    final_inv_no = data['inv_no']
                    is_update = PurchaseMaster.objects.filter(pk=final_inv_no).exists()
                
                purchase_master, created = PurchaseMaster.objects.update_or_create(
                    invno=final_inv_no,
                    defaults={
                        'invdate': data['inv_date'],
                        'party': party,
                        'partyname': data['party_name'],
                        'add1': data.get('add1'),
                        'add2': data.get('add2'),
                        'city': data.get('city'),
                        'mobile': data.get('mobile'),
                        'email': data.get('email', ''),
                        'total': data['sub_total'],
                        'discount_per': data['discount_per'],
                        'discount_amt': data['discount_amt'],
                        'adjustment': data['adjustment'],
                        'net_amount': data['net_amount'],
                        'amount_in_words': data['amount_in_words'],
                        'remark': data['remark']
                    }
                )
                
                # Handle Details
                if not created:
                    purchase_master.details.all().delete()

                items_data = data['items']
                for item_row in items_data:
                    item_obj = Item.objects.get(itemname=item_row['item_name'])
                    PurchaseDetail.objects.create(
                        invno=purchase_master,
                        itemname=item_obj,
                        qty=item_row['qty'],
                        rate=item_row['rate'],
                        itemamt=item_row['amount'],
                        itemremark='' 
                    )
            
            msg = 'Purchase Updated Successfully!' if is_update else 'Purchase Saved Successfully!'
            return JsonResponse({'status': 'success', 'message': msg})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

def purchase_list(request):
    sort = request.GET.get("sort", "-invdate")
    direction = request.GET.get("direction", "desc")
    
    order = sort if direction == "asc" else f"-{sort}"
    if sort == "-invdate":
        order = "-invdate"
        
    purchases = PurchaseMaster.objects.all().order_by(order, '-invno').prefetch_related('details__itemname')
    return render(request, 'transactions/purchase_list.html', {
        'purchases': purchases,
        'current_sort': sort,
        'current_direction': direction
    })

# --- RECEIPT VIEWS ---

def receipt_entry(request, pk=None):
    parties = Party.objects.all().order_by('partyname')
    
    receipt = None
    receipt_data = None
    
    if pk:
        receipt = get_object_or_404(Receipt, pk=pk)
        next_entry = receipt.entry_no
        
        receipt_data = {
            'date': receipt.date.strftime('%Y-%m-%d'),
            'party_name': receipt.party_name,
            'amount': str(receipt.amount),
            'remark': receipt.remark or ''
        }
    else:
        # Generate next Entry Number
        last_entry = Receipt.objects.all().count()
        next_entry = f"REC-{last_entry + 1:04d}"
    
    return render(request, 'transactions/receipt_entry.html', {
        'parties': parties,
        'next_entry': next_entry,
        'receipt': receipt,
        'receipt_data': receipt_data
    })

@csrf_exempt
def save_receipt(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create or Update Receipt
            party = Party.objects.get(partyname=data['party_name'])
            
            receipt, created = Receipt.objects.update_or_create(
                entry_no=data['entry_no'],
                defaults={
                    'date': data['date'],
                    'party': party,
                    'party_name': data['party_name'],
                    'amount': data['amount'],
                    'remark': data['remark']
                }
            )
            
            message = 'Receipt Saved Successfully!' if created else 'Receipt Updated Successfully!'
            return JsonResponse({'status': 'success', 'message': message, 'redirect_url': '/receipt/list/'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

@csrf_exempt
def delete_receipt(request, pk):
    if request.method == 'POST':
        try:
            receipt = Receipt.objects.get(pk=pk)
            receipt.delete()
            return JsonResponse({'status': 'success', 'message': 'Receipt Deleted Successfully!'})
        except Receipt.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Receipt not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

def receipt_list(request):
    sort = request.GET.get("sort", "-date")
    direction = request.GET.get("direction", "desc")
    
    order = sort if direction == "asc" else f"-{sort}"
    if sort == "-date":
        order = "-date"
        
    receipts = Receipt.objects.all().order_by(order, '-entry_no')
    return render(request, 'transactions/receipt_list.html', {
        'receipts': receipts,
        'current_sort': sort,
        'current_direction': direction
    })

# --- PAYMENT VIEWS ---

def payment_entry(request, pk=None):
    parties = Party.objects.all().order_by('partyname')
    
    payment = None
    payment_data = None
    
    if pk:
        payment = get_object_or_404(Payment, pk=pk)
        next_entry = payment.entry_no
        
        payment_data = {
            'date': payment.date.strftime('%Y-%m-%d'),
            'party_name': payment.party_name,
            'amount': str(payment.amount),
            'remark': payment.remark or ''
        }
    else:
        # Generate next Entry Number
        last_entry = Payment.objects.all().count()
        next_entry = f"PAY-{last_entry + 1:04d}"
    
    return render(request, 'transactions/payment_entry.html', {
        'parties': parties,
        'next_entry': next_entry,
        'payment': payment,
        'payment_data': payment_data
    })

@csrf_exempt
def save_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Create or Update Payment
            party = Party.objects.get(partyname=data['party_name'])
            
            payment, created = Payment.objects.update_or_create(
                entry_no=data['entry_no'],
                defaults={
                    'date': data['date'],
                    'party': party,
                    'party_name': data['party_name'],
                    'amount': data['amount'],
                    'remark': data['remark']
                }
            )
            
            message = 'Payment Saved Successfully!' if created else 'Payment Updated Successfully!'
            return JsonResponse({'status': 'success', 'message': message, 'redirect_url': '/payment/list/'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

@csrf_exempt
def delete_payment(request, pk):
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            return JsonResponse({'status': 'success', 'message': 'Payment Deleted Successfully!'})
        except Payment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Payment not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid Request'})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid Request'})

def payment_list(request):
    sort = request.GET.get("sort", "-date")
    direction = request.GET.get("direction", "desc")
    
    order = sort if direction == "asc" else f"-{sort}"
    if sort == "-date":
        order = "-date"
        
    payments = Payment.objects.all().order_by(order, '-entry_no')
    return render(request, 'transactions/payment_list.html', {
        'payments': payments,
        'current_sort': sort,
        'current_direction': direction
    })

def party_ledger(request):
    parties = Party.objects.all().order_by('partyname')
    selected_party_name = request.GET.get('party')
    
    ledger_data = []
    summary = {
        'opening_balance': 0,
        'total_sale': 0,
        'total_purchase': 0,
        'total_receipt': 0,
        'total_payment': 0,
        'closing_balance': 0
    }
    
    if selected_party_name:
        party = get_object_or_404(Party, partyname=selected_party_name)
        
        # Opening Balance
        op_dr = party.openingdr or 0
        op_cr = party.openingcr or 0
        summary['opening_balance'] = op_dr - op_cr
        
        running_balance = summary['opening_balance']
        
        # Fetch Transactions
        sales = SaleMaster.objects.filter(party=party)
        purchases = PurchaseMaster.objects.filter(party=party)
        receipts = Receipt.objects.filter(party=party)
        payments = Payment.objects.filter(party=party)
        
        # Process Sales (Debit)
        for sale in sales:
            summary['total_sale'] += sale.net_amount
            ledger_data.append({
                'date': sale.invdate,
                'entry_no': sale.invno,
                'type': 'Sale',
                'remark': sale.remark,
                'dr_amt': sale.net_amount,
                'cr_amt': 0
            })
            
        # Process Purchases (Credit)
        for purchase in purchases:
            summary['total_purchase'] += purchase.net_amount
            ledger_data.append({
                'date': purchase.invdate,
                'entry_no': purchase.invno,
                'type': 'Purchase',
                'remark': purchase.remark,
                'dr_amt': 0,
                'cr_amt': purchase.net_amount
            })
            
        # Process Receipts (Credit) - Party gives money, so Party Account is Credited
        for receipt in receipts:
            summary['total_receipt'] += receipt.amount
            ledger_data.append({
                'date': receipt.date,
                'entry_no': receipt.entry_no,
                'type': 'Receipt',
                'remark': receipt.remark,
                'dr_amt': 0,
                'cr_amt': receipt.amount
            })
            
        # Process Payments (Debit) - We give money to Party, so Party Account is Debited
        for payment in payments:
            summary['total_payment'] += payment.amount
            ledger_data.append({
                'date': payment.date,
                'entry_no': payment.entry_no,
                'type': 'Payment',
                'remark': payment.remark,
                'dr_amt': payment.amount,
                'cr_amt': 0
            })
            
        # Sort by Date
        ledger_data.sort(key=lambda x: x['date'])
        
        # Calculate Running Balance
        for entry in ledger_data:
            running_balance = running_balance + entry['dr_amt'] - entry['cr_amt']
            entry['balance'] = running_balance
            
        summary['closing_balance'] = running_balance

    return render(request, 'transactions/party_ledger.html', {
        'parties': parties,
        'selected_party': selected_party_name,
        'ledger_data': ledger_data,
        'summary': summary
    })

def party_balance_list(request):
    sort = request.GET.get("sort", "partyname")
    direction = request.GET.get("direction", "asc")
    
    order = sort if direction == "asc" else f"-{sort}"
    
    # Base query
    parties = Party.objects.all()
    
    # We can handle model level sorting here. Calculated fields will be sorted later.
    db_sortable_fields = ['partyname', 'city']
    if sort in db_sortable_fields:
        parties = parties.order_by(order)
    else:
        # Default order if sorting by calculated field, or provide stability
        parties = parties.order_by('partyname')
        
    party_balances = []
    
    total_opening = 0
    total_sale = 0
    total_purchase = 0
    total_receipt = 0
    total_payment = 0
    total_closing = 0

    for party in parties:
        # Opening Balance
        op_dr = party.openingdr or 0
        op_cr = party.openingcr or 0
        opening_bal = op_dr - op_cr
        
        # Transactions
        # Optimizing: Ideally use aggregation, but for simplicity looping as per plan or using aggregate here
        # using aggregate for better performance than loading all objects
        from django.db.models import Sum
        
        sale_sum = SaleMaster.objects.filter(party=party).aggregate(Sum('net_amount'))['net_amount__sum'] or 0
        purchase_sum = PurchaseMaster.objects.filter(party=party).aggregate(Sum('net_amount'))['net_amount__sum'] or 0
        receipt_sum = Receipt.objects.filter(party=party).aggregate(Sum('amount'))['amount__sum'] or 0
        payment_sum = Payment.objects.filter(party=party).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Closing Balance calculation
        # Closing = Opening + Debit (Sale, Payment) - Credit (Purchase, Receipt)
        # Note: 
        # Sale -> Party Debit (We create invoice, they owe us)
        # Purchase -> Party Credit (We receive invoice, we owe them)
        # Receipt -> Party Credit (They pay us, creates Credit entry in their ledger)
        # Payment -> Party Debit (We pay them, creates Debit entry in their ledger)
        
        closing_bal = opening_bal + sale_sum + payment_sum - purchase_sum - receipt_sum
        
        party_balances.append({
            'party': party,
            'opening_balance': opening_bal,
            'total_sale': sale_sum,
            'total_purchase': purchase_sum,
            'total_receipt': receipt_sum,
            'total_payment': payment_sum,
            'closing_balance': closing_bal
        })
        
        # Grant Totals
        total_opening += opening_bal
        total_sale += sale_sum
        total_purchase += purchase_sum
        total_receipt += receipt_sum
        total_payment += payment_sum
        total_closing += closing_bal

    # Sort in memory for calculated fields (op_balance, closing_balance)
    if sort == "opening_balance":
        party_balances.sort(key=lambda x: x['opening_balance'], reverse=(direction == "desc"))
    elif sort == "closing_balance":
        party_balances.sort(key=lambda x: x['closing_balance'], reverse=(direction == "desc"))

    grand_totals = {
        'opening': total_opening,
        'sale': total_sale,
        'purchase': total_purchase,
        'receipt': total_receipt,
        'payment': total_payment,
        'closing': total_closing
    }

    return render(request, 'transactions/party_balance_list.html', {
        'party_balances': party_balances,
        'grand_totals': grand_totals,
        'current_sort': sort,
        'current_direction': direction
    })

def current_stock_report(request):
    sort = request.GET.get("sort", "item_name")
    direction = request.GET.get("direction", "asc")
    
    order = sort if direction == "asc" else f"-{sort}"
    
    items = Item.objects.all()
    if sort == "item_name":
        # Note: Model field is 'itemname'
        items = items.order_by("itemname" if direction == "asc" else "-itemname")
    else:
        items = items.order_by('itemname')
        
    stock_data = []

    from django.db.models import Sum

    for item in items:
        # Opening Stock
        op_stock = getattr(item, 'opening_stock', 0)
        if op_stock is None:
            op_stock = 0

        # Purchase Qty (Sum of PurchaseDetail qty for this item)
        purchase_qty_agg = PurchaseDetail.objects.filter(itemname=item).aggregate(Sum('qty'))['qty__sum']
        purchase_qty = purchase_qty_agg if purchase_qty_agg is not None else 0

        # Sale Qty (Sum of SaleDetail qty for this item)
        sale_qty_agg = SaleDetail.objects.filter(itemname=item).aggregate(Sum('qty'))['qty__sum']
        sale_qty = sale_qty_agg if sale_qty_agg is not None else 0

        # Closing Stock logic: Op + Purchase - Sale
        closing_stock = op_stock + purchase_qty - sale_qty

        stock_data.append({
            'item': item,
            'op_stock': op_stock,
            'purchase_qty': purchase_qty,
            'sale_qty': sale_qty,
            'closing_stock': closing_stock
        })

    # In-memory sort for dynamically calculated columns
    if sort != "item_name":
        reverse_sort = (direction == "desc")
        if sort == "opening_stock":
            stock_data.sort(key=lambda x: x['op_stock'], reverse=reverse_sort)
        elif sort == "purchase_qty":
            stock_data.sort(key=lambda x: x['purchase_qty'], reverse=reverse_sort)
        elif sort == "sale_qty":
            stock_data.sort(key=lambda x: x['sale_qty'], reverse=reverse_sort)
        elif sort == "closing_stock":
            stock_data.sort(key=lambda x: x['closing_stock'], reverse=reverse_sort)

    return render(request, 'transactions/current_stock_list.html', {
        'stock_data': stock_data,
        'current_sort': sort,
        'current_direction': direction
    })

def item_ledger(request):
    items = Item.objects.all().order_by('itemname')
    selected_item_name = request.GET.get('item')
    
    ledger_data = []
    summary = {
        'opening_stock': 0,
        'total_in': 0,
        'total_out': 0,
        'closing_stock': 0
    }
    
    if selected_item_name:
        item = get_object_or_404(Item, itemname=selected_item_name)
        
        # Opening Stock
        summary['opening_stock'] = item.opening_stock or 0
        running_stock = summary['opening_stock']
        
        # Fetch Transactions
        # Sale -> Out
        # Purchase -> In
        sale_details = SaleDetail.objects.filter(itemname=item).select_related('invno')
        purchase_details = PurchaseDetail.objects.filter(itemname=item).select_related('invno')
        
        # Process Sales (Out)
        for detail in sale_details:
            summary['total_out'] += detail.qty
            ledger_data.append({
                'date': detail.invno.invdate,
                'inv_no': detail.invno.invno,
                'type': 'Sale',
                'party': detail.invno.partyname,
                'in_qty': 0,
                'out_qty': detail.qty,
                'rate': detail.rate
            })
            
        # Process Purchases (In)
        for detail in purchase_details:
            summary['total_in'] += detail.qty
            ledger_data.append({
                'date': detail.invno.invdate,
                'inv_no': detail.invno.invno,
                'type': 'Purchase',
                'party': detail.invno.partyname,
                'in_qty': detail.qty,
                'out_qty': 0,
                'rate': detail.rate
            })
            
        # Sort by Date
        ledger_data.sort(key=lambda x: x['date'])
        
        # Calculate Running Stock
        for entry in ledger_data:
            running_stock = running_stock + entry['in_qty'] - entry['out_qty']
            entry['balance'] = running_stock
            
        summary['closing_stock'] = running_stock

    return render(request, 'transactions/item_ledger.html', {
        'items': items,
        'selected_item': selected_item_name,
        'ledger_data': ledger_data,
        'summary': summary
    })
