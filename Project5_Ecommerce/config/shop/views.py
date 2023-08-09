from django.shortcuts import render, get_object_or_404

from .models import *
from cart.forms import AddProductFrom
# Create your views here.
# product_in_category: 카테고리 페이지
#                      URL로부터 category_slug를 찾아서 현재 어느 카테고리를 보여주는 것인지 판단. 만약 선택한 카테고리가 없을 경우 전체 상품 목록을 노출
def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True) # 노출할 제품도 처음에는 모든 제품 목록을 준비

    if category_slug: # category_slug이 존재한다면
        current_category = get_object_or_404(Category, slug=category_slug) # category_slug에 해당하는 카테고리를 선택하고
        products = products.filter(category=current_category) # 그 카테고리에 속한 제품들로 필터링
    
    return render(request, 'shop/list.html', {'current_category':current_category, 'categories':categories, 'products':products})

# product_detail: 제품 상세 뷰
def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    add_to_cart = AddProductFrom(initial={'quantity': 1})

    return render(request, 'shop/detail.html', {'product': product, 'add_to_cart': add_to_cart})