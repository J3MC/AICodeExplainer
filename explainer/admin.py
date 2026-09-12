from django.contrib import admin

from .models import Explanation


admin.site.site_header = "AI Code Explainer Admin"
admin.site.site_title = "AI Code Explainer Admin"
admin.site.index_title = "Workspace control center"


@admin.register(Explanation)
class ExplanationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "language",
        "created_at",
    )
    list_filter = (
        "language",
        "created_at",
    )
    search_fields = (
        "user__username",
        "code",
        "explanation",
    )
    date_hierarchy = "created_at"
    list_per_page = 25
    readonly_fields = ("created_at",)
