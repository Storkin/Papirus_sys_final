from django import forms
from .models import Product, Customer


def _to_float(value, default=0.0):
    """'5,50' / '1.500,00' / '5.5' -> float (Türkçe virgül desteği)."""
    v = str(value).strip()
    if not v:
        return default
    if ',' in v and '.' in v:
        v = v.replace('.', '').replace(',', '.')
    elif ',' in v:
        v = v.replace(',', '.')
    return float(v)


class ProductForm(forms.ModelForm):
    # Fiyat ve KDV virgülle de yazılabilsin (5,50 gibi)
    price = forms.CharField(
        label='Fiyat (₺)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0,00', 'inputmode': 'decimal', 'autocomplete': 'off'})
    )
    tax_rate = forms.CharField(
        required=False, label='KDV Oranı (%)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20', 'inputmode': 'decimal', 'autocomplete': 'off'})
    )

    def clean_price(self):
        try:
            val = _to_float(self.cleaned_data.get('price', ''))
        except ValueError:
            raise forms.ValidationError('Geçerli bir fiyat giriniz. Örnek: 5,50')
        if val < 0:
            raise forms.ValidationError('Fiyat negatif olamaz.')
        return val

    def clean_tax_rate(self):
        v = self.cleaned_data.get('tax_rate', '')
        if not str(v).strip():
            return 20.0
        try:
            return _to_float(v, 20.0)
        except ValueError:
            raise forms.ValidationError('Geçerli bir KDV oranı giriniz.')

    class Meta:
        model = Product
        fields = [
            'name', 'category', 'price', 'manufacturer',
            'stock_quantity', 'unit', 'barcode',
            'tax_rate', 'supplier', 'shelf_location', 'min_stock'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'adet, kutu, paket...'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'shelf_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'A1, B3...'}),
            'min_stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CustomerForm(forms.ModelForm):

    # FloatField Django kendi doğrulamasını yapmadan önce hata verdiği için
    # debt'i CharField olarak tanımlıyoruz, clean_debt'te float'a çeviriyoruz
    debt = forms.CharField(
        required=False,
        label='Borç (₺)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0,00',
            'autocomplete': 'off',
        })
    )

    def clean_debt(self):
        value = self.cleaned_data.get('debt', '')
        if not value or str(value).strip() == '':
            return 0.0
        value = str(value).strip()
        if ',' in value and '.' in value:
            value = value.replace('.', '').replace(',', '.')
        elif ',' in value:
            value = value.replace(',', '.')
        try:
            result = float(value)
            if result < 0:
                raise forms.ValidationError("Borç miktarı negatif olamaz.")
            return result
        except ValueError:
            raise forms.ValidationError("Geçerli bir tutar giriniz. Örnek: 1.500,00")

    class Meta:
        model = Customer
        fields = ['name', 'shop_name', 'phone', 'email', 'address', 'tax_number', 'contact_person', 'debt', 'debt_due_date', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'shop_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0212 000 00 00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tax_number': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'debt_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
