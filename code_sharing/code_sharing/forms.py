from django import forms
from .models import Code, Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '2',
                   'placeholder': 'Write some comments...',
                   'value': 'none',
                   'class': 'form-control mt-1 mb-3',
                   }
        ))

    class Meta:
        model = Comment
        fields = ['content']


class CodePaste(forms.ModelForm):
    snippet = forms.CharField(
        label = '',
        widget=forms.Textarea(
            attrs={'rows': '2',
                   'placeholder': 'Paste your code here...',
                   'value': 'none',
                   'class': 'form-control mt-1 mb-3',
                   }
        ))
    class Meta:
        model = Code
        fields = ['snippet']

    