from django.contrib import admin

from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)} # prepopulated_fields: slug 필드는 name 필드의 값에 따라 자동으로 설정

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available_display', 'available_order', 'created', 'updated']
    list_filter = ['available_display', 'created', 'updated', 'category']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'available_display', 'available_order'] # list_editable: 목록에서 주요 값들의 변경 가능

admin.site.register(Product, ProductAdmin)