from django.contrib import admin
from .models import SaleMaster, SaleDetail, PurchaseMaster, PurchaseDetail

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 1

class SaleMasterAdmin(admin.ModelAdmin):
    inlines = [SaleDetailInline]
    list_display = ('invno', 'invdate', 'party', 'net_amount')
    search_fields = ('invno', 'party__name')

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1

class PurchaseMasterAdmin(admin.ModelAdmin):
    inlines = [PurchaseDetailInline]
    list_display = ('invno', 'invdate', 'party', 'net_amount')
    search_fields = ('invno', 'party__name')

admin.site.register(SaleMaster, SaleMasterAdmin)
admin.site.register(PurchaseMaster, PurchaseMasterAdmin)

