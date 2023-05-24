from distutils.command.upload import upload
from tabnanny import verbose
from tkinter import CASCADE
from unicodedata import name
from django.db import models

from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True) # db_index=True: 테이블에서 해당 이름의 열을 인덱스 열로 설정
    meta_description = models.TextField(blank=True) # meta_description: SEO(Search Engine Optimization)을 위해 만드는 필드
    # SlugField: 현재 프로젝트에서는 상품명 등을 이용해서 URL을 만드는 방식
    # allow_unicode: 영문을 제외한 다른 언어도 값으로 사용할 수 있게 하는 옵션
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        # verbose_name/verbose_name_plural: 관리자 페이지에서 보여지는 객체가 단수일 때와 복수일 때 표현하는 값을 결정
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_in_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products') # 카테고리를 삭제해도 보통은 상품이 남아있어야 하기 때문에 on_delete를 SET_NULL로 설정, 이때 당연히 null값이 저장될 수 있어야 하기 때문에 null=True로 설정
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    available_display = models.BooleanField('Display', default=True) # 상품 노출 여부
    available_order = models.BooleanField('Order', default=True) # 상품 주문 가능 여부

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id', 'slug']] # index_together: 멀티 컬럼 색인 기능 -> id와 slug 필드를 묶어서 색인이 가능하도록 하는 옵션
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])