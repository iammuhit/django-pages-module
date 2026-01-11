from django.contrib import admin

from app.modules.pages.models import Page, Type


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'type__name', 'is_enabled', 'publish_at', 'created_at', 'updated_at']
    readonly_fields = ['route_name']
    prepopulated_fields = {'slug': ['title']}

    fieldsets = [
        ('General', {
            'fields': ['type', 'title', 'slug', 'content'],
        }),

        ('SEO', {
            'classes': ['collapse'],
            'fields': ['meta_title', 'meta_description', 'meta_keywords'],
        }),
        
        ('Options', {
            'classes': ['collapse'],
            'fields': ['is_enabled', 'publish_at', 'is_home', 'is_visible', 'is_exact', 'parent', 'route_name'],
        }),
    ]
