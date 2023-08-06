from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from ..models import Question, Answer

@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user) # Question 모델의 voter 필드는 ManyToManyField로 정의했으므로 question.voter.add(request.user)와 같이 add 함수로 추천인을 추가해야 한다.
    return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user) # Question 모델의 voter 필드는 ManyToManyField로 정의했으므로 question.voter.add(request.user)와 같이 add 함수로 추천인을 추가해야 한다.
    return redirect('pybo:detail', question_id=answer.question.id)