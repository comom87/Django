from decimal import Decimal

from django.conf import settings

from shop.models import Product
from coupon.models import Coupon

# Cart 기능: 선택한 제품을 주문하기 위해 보관하는 기능
#            이 기능은 보통 데이터베이스에 저장하는 방식으로 만들지만 세션 기능을 활용해 만들기도 한다.
#            세션으로 사용하는 방식이기 때문에 request.session에 데이터를 저장하고 꺼내오는 방식
class Cart(object):
    def __init__(self, request):
        self.session = request.session # request.session에 데이터를 저장하고 꺼내온다.
        cart = self.session.get(settings.CART_ID) # 세션에 값을 저장하려면 키 값을 설정해야 한다.
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def __iter__(self):
        product_ids = self.cart.keys()

        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            self.cart[str(product.id)]['product'] = product
        
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']

            yield item
    
    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if is_update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    # save(): 장바구니에 상품을 담을 때 사용
    def save(self):
        self.session[settings.CART_ID] = self.cart
        self.session.modified = True
    
    # remove(): 장바구니에 상품을 삭제할 때 사용
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del(self.cart[product_id])
            self.save()
    
    # clear(): 장바구니를 비우는 기능. 주문을 완료했을 때도 사용.
    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session['coupon_id'] = None
        self.session.modified = True
    
    # get_product_total(): 장바구니에 담긴 상품의 총 가격을 계산
    def get_product_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None
    
    # get_discount_total(): 할인 금액
    def get_discount_total(self):
        if self.coupon:
            if self.get_product_total() >= self.coupon.amount:
                return self.coupon.amount
        return Decimal(0)
    
    # get_total_price(): 할인 이후 총 금액
    def get_total_price(self):
        return self.get_product_total() - self.get_discount_total()