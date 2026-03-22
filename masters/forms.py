from django import forms
from .models import Party, Item, Company, Category

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = '__all__'
        widgets = {
            'partyname': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'add1': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'add2': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'city': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm'}),
            'openingdr': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'openingcr': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'remark': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 3}),
        }

class ItemForm(forms.ModelForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all().order_by('companyname'), required=False, widget=forms.Select(attrs={'class': 'form-select form-select-sm select2'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all().order_by('categoryname'), required=False, widget=forms.Select(attrs={'class': 'form-select form-select-sm select2'}))
    
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'itemname': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'opening_stock': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'sale_rate': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'purchase_rate': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'reorder': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'remark': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': 2}),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'companyname': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'categoryname': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }
