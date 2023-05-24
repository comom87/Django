from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from polls.models import Question, Choice

# Create your views here.
def index(request): # 뷰 함수를 정의. request 객체는 뷰 함수의 필수 인자.
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    # 템플릿에게 넘겨줄 객체의 이름은 latest_question_list.
    # latest_question_list 객체는 Question 테이블 객체에서 pub_date 컬럼의 역순으로 정렬하여 5개의 최근 Question 객체를 가져와서 만듭니다.
    context = {'latest_question_list': latest_question_list}
    # 템플릿에 넘겨주는 방식은 파이썬 사전 타입으로, 템플리셍 사용될 변수명과 그 변수명에 해당하는 객체를 매핑하는 사전으로 context 변수를 만들어서 이를 render() 함수에 보내줍니다.
    return render(request, 'polls/index.html', context)
    # render() 함수는 템플릿 파일인 polls/index.html에 context 변수를 적용하여 사용자에게 보여줄 최종 HTML 텍스트를 만들고, 이를 담아서 HttpResponse 객체를 반환합니다.
    # index() 뷰 함수는 최종적으로 클라이언트에게 응답할 데이터인 HttpResponse 객체를 반환

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})