from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Code, Comment, Reply
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView
from .forms import CodeForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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
        comments = Comment.objects.filter(code_origin=code).order_by('-date_posted')
        # reply_form = ReplyForm()

        context = {
            'code': code,
            'comment_form': comment_form,
            'comments': comments,
            # 'reply_form': reply_form,
        }

        return render(request, 'codeapp/code_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        code = Code.objects.get(pk=pk)
        
        print('comment_submit' in request.POST)
        
        comment_form = CommentForm(request.POST)
        # reply_form = ReplyForm()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.code_origin = code
            new_comment.save()
        
        comment_form = CommentForm()
        
        comments = code.comments.all().order_by('-date_posted')
        context = {
            'code': code,
            'comment_form': comment_form,
            'comments': comments,
            # 'reply_form': reply_form,
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
    fields = ['title', 'snippet', 'description']
    
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
    success_url = '/my_codes/'

    def test_func(self):
        code = self.get_object()
        if self.request.user == code.author:
            return True
        return False
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']
    template_name = 'codeapp/comment_form_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        code = get_object_or_404(Code, pk=comment.code_origin.pk)
        return reverse('codeapp-code-detail', args=[code.pk])

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return context

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author or self.request.user == comment.code_origin.author:
            return True
        return False
    
    def get_success_url(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        code = get_object_or_404(Code, pk=comment.code_origin.pk)
        return reverse('codeapp-code-detail', args=[code.pk])


@login_required
def my_codes(request):
    code = Code.objects.filter(author=request.user).order_by('-date_posted')
    context = {
        'codes': code,
    }
    return render(request, 'codeapp/my_codes.html', context)

