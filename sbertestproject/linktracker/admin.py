from django.contrib import admin
from linktracker.models import VisitedLink

# Register your models here.
class VisitedLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'link', 'visited_at']


admin.site.register(VisitedLink, VisitedLinkAdmin)