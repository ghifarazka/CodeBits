from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Code, Comment, Folder
from .forms import CommentForm, CodePaste

# Create your views here.
def home(request):
    return render(request, 'code_sharing/home.html')

def mycodes(request):
    return HttpResponse('<h1>Explore your codes</h1>')

def index(request):
    return render(request, 'code_sharing/index.html')

class CodeCreateView(LoginRequiredMixin, CreateView):
    model = Code
    fields = ['title', 'snippet']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class CodeListView(ListView):
    model = Code
    
class CodeDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        Codes = Code.objects.get(pk=pk)
        self.current_code = Codes

        code_paste = CodePaste()
        komentar = Comment.objects.filter(code_origin=Codes).order_by('-date_posted')
        jawaban = Reply.objects.filter(comment_origin=comment).order_by('-date_posted')

        context = {
            'Code': Codes,
            'form': code_paste,
            'Comment': komentar,
            'Reply': jawaban,
        }

        return render(request, 'code_sharing/code_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        Codes = Code.objects.get(pk=pk)

        code_paste = CodePaste(request.POST)
        if code_paste.is_valid():
            new_code = code_paste.save(commit=False)
            new_code.author = request.user
            new_code.code_origin = Codes
            new_code.save()

        code_paste = CodePaste()

        komentar = Comment.objects.filter(code_origin=Codes).order_by('-date_posted')
        jawaban = Reply.objects.filter(comment_origin=comment).order_by('-date_posted')

        context = {
            'Code': Codes,
            'form': code_paste,
            'Comment': komentar,
            'Reply': jawaban,
        }

        return render(request, 'code_sharing/code_detail.html', context)