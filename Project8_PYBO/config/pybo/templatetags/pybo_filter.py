# 템플릿 필터 함수는 템플릿 필터 파일을 작성한 다음에 정의

from django import template

register = template.Library()

@register.filter # @register.filter 애너테이션: 템플릿에서 해당 함수를 필터롤 사용
def sub(value, arg):
    return value - arg