from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Bookmark
# Create your views here.
class BookmarkListView(ListView):
    model = Bookmark
    paginate_by = 6 # paginate_by: 한 페이지에 몇 개씩 출력할 것인지 결정하는 값

class BookmarkCreateView(CreateView):
    model = Bookmark
    fields = ['site_name', 'url'] # fields: 어떤 변수를 입력받을 것인지 설정하는 부분
    success_url = reverse_lazy('list') # success_url: 글쓰기를 완료하고 이동할 페이지
    template_name_suffix = '_create' # template_name_suffix: 사용할 템플릿의 접미사만 변경하는 설정값

    # 기본으로 설정되어 있는 템플릿 이름들은 모델명_xxx
    # ex) CreateView와 UpdateView는 form이 접미사

class BookmarkDetailView(DetailView):
    model = Bookmark

class BookmarkUpdateView(UpdateView):
    model = Bookmark
    fields = ['site_name', 'url']
    template_name_suffix = '_update'

class BookmarkDeleteView(DeleteView):
    model = Bookmark
    success_url = reverse_lazy('list')