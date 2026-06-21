from django.contrib import admin
from .models import Product, Customer, Sale, SaleItem, StockMovement, ReferenceBarcode


@admin.register(ReferenceBarcode)
class ReferenceBarcodeAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'name', 'manufacturer', 'category', 'unit', 'updated_at')
    search_fields = ('barcode', 'name', 'manufacturer', 'category')
    list_filter = ('category', 'manufacturer')


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(StockMovement)
