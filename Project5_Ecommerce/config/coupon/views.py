from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Coupon
from .forms import AddCouponForm

# Create your views here.
@require_POST
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']

        try:
            # get 메서드나 filter 메서드를 사용해 원하는 데이터를 찾을 때는 각 '필드명__옵션' 형태로 질의를 만들 수 있다.
            # iexact: 대소문자 구분없이 일치하는 코드를 찾는다.
            # use_from이 현재 시간보다 이전이어야 하므로 __lte 옵션 사용
            # use_to는 현재 시간보다 이후여야 하므로 __gte 옵션 사용
            coupon = Coupon.objects.get(code__iexact=code, use_from__lte=now, use_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:detail')