from django import forms
from django.utils.translation import gettext_lazy as _


class NewsAnalysisForm(forms.Form):
    news_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control news-textarea',
            'placeholder': _('Paste the news article or text here to analyze...'),
            'rows': 8,
            'id': 'newsText',
        }),
        min_length=30,
        max_length=5000,
        label=_('News Text'),
        error_messages={
            'min_length': _('Please enter at least 30 characters.'),
            'max_length': _('Text must be under 5000 characters.'),
            'required': _('This field is required.'),
        }
    )
