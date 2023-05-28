from django.http import HttpResponse
from django.shortcuts import render

from .models import Code, Comment
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView
from .forms import CodeForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

# def index(request):
#     context = {
#         'codes': Code.objects.all()
#     }
#     return render(request, 'codeapp/index.html', context)

class CodeListView(ListView):
    model = Code
    template_name = 'codeapp/index.html'
    context_object_name = 'codes'
    ordering = ['-date_posted']

class CodeDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        code = Code.objects.get(pk=pk)
        self.current_code = code

        comment_form = CommentForm()
        comment = Comment.objects.filter(code_origin=code).order_by('-date_posted')

        context = {
            'code': code,
            'form': comment_form,
            'comments': comment,
        }

        return render(request, 'codeapp/code_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        code = Code.objects.get(pk=pk)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.code_origin = code
            new_comment.save()

        comment_form = CommentForm()

        comment = Comment.objects.filter(code_origin=code).order_by('-date_posted')

        context = {
            'code': code,
            'form': comment_form,
            'comments': comment,
        }

        return render(request, 'codeapp/code_detail.html', context)

class CodeCreateView(LoginRequiredMixin, CreateView):
    model = Code
    
    def get_form_class(self):
        return CodeForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CodeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Code
    fields = ['title', 'description', 'snippet']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        code = self.get_object()
        if self.request.user == code.author:
            return True
        return False

class CodeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Code
    success_url = '/codeapp/my_codes/'

    def test_func(self):
        code = self.get_object()
        if self.request.user == code.author:
            return True
        return False

@login_required
def my_codes(request):
    code = Code.objects.filter(author=request.user).order_by('-date_posted')
    context = {
        'codes': code,
    }
    return render(request, 'codeapp/my_codes.html', context)