from django.db import models

class Party(models.Model):
    partyname = models.CharField(max_length=255, primary_key=True)
    add1 = models.CharField(max_length=255, blank=True, null=True)
    add2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    openingdr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    openingcr = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.partyname

class Company(models.Model):
    companyname = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.companyname


class Category(models.Model):
    categoryname = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.categoryname


class Item(models.Model):
    itemname = models.CharField(max_length=255, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    opening_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sale_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    purchase_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reorder = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.itemname


