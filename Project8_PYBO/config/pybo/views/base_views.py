from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question
from django.core.paginator import Paginator
from django.db.models import Q, Count

def index(request): # request: 장고에 의해 자동으로 전달되는 HTTP 요청 객체
    page = request.GET.get('page', '1') # get('page', '1')에서 '1'은 /pybo/처럼 ?page=1과 같은 page 파라미터가 없는 URL을 위해 기본값으로 1을 지정한 것
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    if so == 'recommend':
        question_list = Question.objects.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = Question.objects.order_by('-create_date')

    # order_by: 조회한 데이터를 특정 속성으로 정렬
    # -create_date: - 기호가 앞에 붙어 있으므로 작성일시의 역순을 의미
    # question_list = Question.objects.order_by('-create_date')

    # subject__icontains=kw: 제목에 kw 문자열이 포함되었는지를 의미
    # answer__author__username__icontains=kw: 답변을 작성한 사람의 이름에 포함되는지를 의미
    # filter 함수에서 모델 필드에 접근하려면 __를 이용

    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()
    # Paginator 클래스: question_list를 페이징 객체 paginator로 변환.
    # 두 번째 파라미터인 10: 페이지당 보여줄 게시물 개수

    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    # print(page_obj)
    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so} # 입력받은 page와 kw값을 템플릿 searchForm에 전달하기 위해 context 안에 'page', 'kw'를 각각 page, kw으로 추가했다.
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id): # question_id: URL 매핑에 있던 question_id
    question = get_object_or_404(Question, pk=question_id) # get_object_or_404 함수: 모델의 기본키를 이용하여 모델 객체 한 건을 반환. pk에 해당하는 건이 없으면 오류 대신 404 페이지를 반환.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)