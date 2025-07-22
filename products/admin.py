from django.contrib import admin
from .models import Product,Contact,CartItem,ProductDetails

class ProductDetailsInline(admin.TabularInline):
    model = ProductDetails
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','discount_price','original_price','stock','category','modified_date','is_available')
    prepopulated_fields = { 'slug': ('product_name',)}
    inlines = [ProductDetailsInline]
    filter_horizontal = ('colors' ,)

admin.site.register(Product, ProductAdmin) 
 
admin.site.register(Contact) 

admin.site.register(CartItem)
admin.site.register(ProductDetails)
