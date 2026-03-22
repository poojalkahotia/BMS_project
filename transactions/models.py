from django.db import models
from masters.models import Party, Item

class SaleMaster(models.Model):
    invno = models.CharField(max_length=50, primary_key=True)
    invdate = models.DateField()
    
    # Party Link
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    
    # Snapshot Fields (Address & Contact at time of sale)
    partyname = models.CharField(max_length=255, blank=True, null=True)
    add1 = models.CharField(max_length=255, blank=True, null=True)
    add2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Financials
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    amount_in_words = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.invno

class SaleDetail(models.Model):
    # Invno (Link to SaleMaster) -> Renamed from 'sale'
    invno = models.ForeignKey(SaleMaster, on_delete=models.CASCADE, related_name='details') 
    
    # itemname (Link to Item)
    itemname = models.ForeignKey(Item, on_delete=models.PROTECT)
    
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    itemamt = models.DecimalField(max_digits=12, decimal_places=2)
    itemremark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.invno} - {self.itemname}"

class PurchaseMaster(models.Model):
    invno = models.CharField(max_length=50, primary_key=True)
    invdate = models.DateField()
    
    # Party Link
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    
    # Snapshot Fields (Address & Contact at time of purchase)
    partyname = models.CharField(max_length=255, blank=True, null=True)
    add1 = models.CharField(max_length=255, blank=True, null=True)
    add2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # Financials
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_per = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    discount_amt = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    adjustment = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    amount_in_words = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.invno

class PurchaseDetail(models.Model):
    # Invno (Link to PurchaseMaster)
    invno = models.ForeignKey(PurchaseMaster, on_delete=models.CASCADE, related_name='details') 
    
    # itemname (Link to Item)
    itemname = models.ForeignKey(Item, on_delete=models.PROTECT)
    
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    itemamt = models.DecimalField(max_digits=12, decimal_places=2)
    itemremark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.invno} - {self.itemname}"

class Receipt(models.Model):
    entry_no = models.CharField(max_length=50, primary_key=True)
    date = models.DateField()
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    party_name = models.CharField(max_length=255, blank=True, null=True) # Snapshot
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.entry_no} - {self.party_name}"

class Payment(models.Model):
    entry_no = models.CharField(max_length=50, primary_key=True)
    date = models.DateField()
    party = models.ForeignKey(Party, on_delete=models.PROTECT)
    party_name = models.CharField(max_length=255, blank=True, null=True) # Snapshot
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    remark = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.entry_no} - {self.party_name}"
