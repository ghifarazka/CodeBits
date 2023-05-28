from django import forms
from .models import Code, Comment

class CodeForm(forms.ModelForm):
    snippet = forms.CharField(widget=forms.Textarea(attrs={'class': 'newcode-form-code'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'newcode-form-desc'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Add an interesting title'
        self.fields['snippet'].widget.attrs['placeholder'] = 'Write or paste your code here'
        self.fields['description'].widget.attrs['placeholder'] = 'Describe your code'
        self.fields['title'].label = False
        self.fields['snippet'].label = False
    
    class Meta:
        model = Code
        fields = ['title', 'snippet', 'description']

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