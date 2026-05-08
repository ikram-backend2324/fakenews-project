from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Analysis(models.Model):
    VERDICT_CHOICES = [
        ('fake', _('Fake')),
        ('real', _('Real')),
        ('uncertain', _('Uncertain')),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='analyses', null=True, blank=True
    )
    news_text = models.TextField(_('News Text'))
    verdict = models.CharField(
        _('Verdict'), max_length=20,
        choices=VERDICT_CHOICES, blank=True
    )
    confidence = models.IntegerField(_('Confidence (%)'), default=0)
    reasoning = models.TextField(_('AI Reasoning'), blank=True)
    language_used = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(default=0.0)

    class Meta:
        verbose_name = _('Analysis')
        verbose_name_plural = _('Analyses')
        ordering = ['-created_at']

    def __str__(self):
        snippet = self.news_text[:60] + '...' if len(self.news_text) > 60 else self.news_text
        return f"[{self.verdict.upper()}] {snippet}"

    def get_verdict_color(self):
        colors = {
            'fake': 'danger',
            'real': 'success',
            'uncertain': 'warning',
        }
        return colors.get(self.verdict, 'secondary')

    def get_verdict_icon(self):
        icons = {
            'fake': 'fa-times-circle',
            'real': 'fa-check-circle',
            'uncertain': 'fa-question-circle',
        }
        return icons.get(self.verdict, 'fa-circle')
