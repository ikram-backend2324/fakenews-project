from django.contrib import admin
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'verdict', 'confidence', 'language_used', 'created_at')
    list_filter = ('verdict', 'language_used', 'created_at')
    search_fields = ('user__username', 'news_text', 'reasoning')
    readonly_fields = ('created_at', 'processing_time')
    ordering = ('-created_at',)

    fieldsets = (
        ('News Content', {
            'fields': ('user', 'news_text', 'language_used')
        }),
        ('AI Result', {
            'fields': ('verdict', 'confidence', 'reasoning', 'processing_time')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
