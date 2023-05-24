from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
 # decorators: 함수형 뷰에서 사용
 #             함수형 뷰의 바로 윗줄에 작성
from django.contrib.auth.decorators import login_required
 # mixins: 클래스형 뷰에서 사용
 #         클래스형 뷰의 첫 번째로 상속
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Photo
# Create your views here.
@login_required
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'photo/list.html', {'photos': photos})

class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/upload.html' # template_name: 실제 사용할 템플릿을 설정

    # form_valid(): 업로드를 끝낸 후 이동할 페이지를 호출하기 위해 사용하는 메서드
    #               현재는 이 메서드를 오버라이드해서 작성자를 설정하는 기능을 추가
    def form_valid(self, form):
        form.instance.author_id = self.request.user.id # 작성자는 현재 로그인 한 사용자로 설정
        if form.is_valid(): # is_valid(): 입력된 값들을 검증
            form.instance.save() # 이상이 없다면 데이터베이스에 저장
            return redirect('/') # redirect 메서드를 이용해 메인 페이지로 이동
        else:
            return self.render_to_response({'form': form}) # 이상이 있다면 작성된 내용을 그대로 작성 페이지에 표시

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = '/'
    template_name = 'photo/delete.html'

class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['photo', 'text']
    template_name = 'photo/update.html'