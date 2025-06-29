from django.contrib import admin
from django.db.models import Count
from .models import Comment

class HasReportsFilter(admin.SimpleListFilter):
    title = 'has reports'
    parameter_name = 'has_reports'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Has reports'),
            ('0', 'No reports'),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.annotate(report_count=Count('reported_by')).filter(report_count__gt=0)
        if self.value() == '0':
            return queryset.annotate(report_count=Count('reported_by')).filter(report_count=0)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'content_preview', 'is_spam', 'report_count', 'created_at')
    list_filter = ('is_spam', HasReportsFilter)  # Use our custom filter
    search_fields = ('content', 'author__username')
    
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Content'
    
    def report_count(self, obj):
        return obj.reported_by.count()
    report_count.short_description = '# Reports'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            report_count=Count('reported_by')
        )

admin.site.register(Comment, CommentAdmin)