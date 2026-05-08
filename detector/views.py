from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import get_language
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .forms import NewsAnalysisForm
from .models import Analysis
from .ai_service import analyze_news


@login_required
def analyze_view(request):
    form = NewsAnalysisForm()
    recent = Analysis.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'detector/analyze.html', {
        'form': form,
        'recent_analyses': recent,
    })


@login_required
@require_POST
def run_analysis(request):
    """AJAX endpoint: receives text, calls AI, saves result, returns JSON."""
    form = NewsAnalysisForm(request.POST)
    if not form.is_valid():
        errors = {}
        for field, error_list in form.errors.items():
            errors[field] = [str(e) for e in error_list]
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    text = form.cleaned_data['news_text']
    lang = get_language() or 'en'

    result = analyze_news(text, lang)

    analysis = Analysis.objects.create(
        user=request.user,
        news_text=text,
        verdict=result['verdict'],
        confidence=result['confidence'],
        reasoning=result['reasoning'],
        language_used=lang,
        processing_time=result.get('processing_time', 0),
    )

    return JsonResponse({
        'success': True,
        'analysis_id': analysis.id,
        'verdict': analysis.verdict,
        'confidence': analysis.confidence,
        'reasoning': analysis.reasoning,
        'verdict_color': analysis.get_verdict_color(),
        'verdict_icon': analysis.get_verdict_icon(),
        'error': result.get('error', False),
    })


@login_required
def history_view(request):
    analyses = Analysis.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'detector/history.html', {
        'analyses': analyses,
    })


@login_required
def analysis_detail(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk, user=request.user)
    return render(request, 'detector/detail.html', {
        'analysis': analysis,
    })
