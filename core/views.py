from django.shortcuts import render
from detector.models import Analysis


def home_view(request):
    stats = {}
    if request.user.is_authenticated:
        user_analyses = Analysis.objects.filter(user=request.user)
        stats = {
            'total': user_analyses.count(),
            'fake': user_analyses.filter(verdict='fake').count(),
            'real': user_analyses.filter(verdict='real').count(),
            'uncertain': user_analyses.filter(verdict='uncertain').count(),
        }
    global_stats = {
        'total': Analysis.objects.count(),
        'fake': Analysis.objects.filter(verdict='fake').count(),
        'real': Analysis.objects.filter(verdict='real').count(),
    }
    return render(request, 'core/home.html', {
        'stats': stats,
        'global_stats': global_stats,
    })


def about_view(request):
    return render(request, 'core/about.html')
