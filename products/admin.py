from django.contrib import admin
from .models import (
                Product,
                Category, 
                ProductImage, 
                ColorVariant, 
                SizeVariant, 
                DeliveryTo,
                Coupon
                
                
                )
# Register your models here.
admin.site.register(Category)

# admin.site.register(Product)
# admin.site.register(ProductImage)

#making a stack of our model ProductImage
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

# then making an admin model of our stack above
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    list_display = ['product_name', 'price', ]

@admin.register(SizeVariant)
class SizeVariantAdmin(admin.ModelAdmin):
    model = SizeVariant
    list_display = ['size_name', 'price']
    

@admin.register(ColorVariant)
class ColorVariant(admin.ModelAdmin):
    model = ColorVariant
    list_display = ['color_name', 'price']

@admin.register(DeliveryTo)
class DeliveryToAdmin(admin.ModelAdmin):
    model = DeliveryTo
    list_display = ["country_name", 'price']
    

# admin.site.register(Product)
admin.site.register(Product, ProductAdmin)
# admin.site.register(ProductAdmin)
admin.site.register(ProductImage)


admin.site.register(Coupon)

