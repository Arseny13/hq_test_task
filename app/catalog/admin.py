from django.contrib import admin

from catalog.models import Product, ProductAccess


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductAccess)
class ProductAccessInfoAdmin(admin.ModelAdmin):
    pass
