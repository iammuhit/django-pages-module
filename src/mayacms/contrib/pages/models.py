from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Type(models.Model):
    name        = models.CharField(max_length=25, unique=True)
    slug        = models.SlugField(max_length=25, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(default=timezone.now)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pages_types'
        verbose_name = _('type')
        verbose_name_plural = _('types')
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('app.modules.pages:types.view', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Page(models.Model):
    title      = models.CharField(max_length=255, unique=True)
    slug       = models.SlugField(max_length=255, unique=True)
    path       = models.CharField(max_length=255, unique=True, editable=False)
    route_name = models.CharField(max_length=255, unique=True, editable=True)
    content    = models.TextField(blank=True)

    is_enabled = models.BooleanField(default=True, verbose_name='Enabled', help_text='Is this page enabled?')
    is_home    = models.BooleanField(default=False, verbose_name='Home Page', help_text='The home page is the default landing page for the website.')
    is_visible = models.BooleanField(default=True, verbose_name='Visible', help_text='Disable to hide this page from page based navigation <strong>structure</strong>.')
    is_exact   = models.BooleanField(default=False, verbose_name='Exact URI', help_text='Disable to allow custom parameters following the URI for this page.')

    type       = models.ForeignKey(Type, on_delete=models.CASCADE)
    parent     = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', editable=True, null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='moderator', editable=False, null=True, on_delete=models.SET_NULL)

    order      = models.IntegerField(editable=False, default=0, verbose_name='Order')
    publish_at = models.DateTimeField(editable=True, default=timezone.now, verbose_name='Publish Date')
    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(editable=False, auto_now=True, verbose_name='Updated')

    meta_title       = models.CharField(max_length=255, blank=True, null=True, verbose_name='Meta Title')
    meta_description = models.TextField(blank=True, null=True, verbose_name='Meta Description')
    meta_keywords    = models.TextField(blank=True, null=True, verbose_name='Meta Keywords')

    class Meta:
        db_table = 'pages_pages'
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        indexes = [
            models.Index(fields=['parent', 'order']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        if self.is_home:
            return reverse('app.modules.pages:pages.home')
        
        return reverse('app.modules.pages:pages.view', kwargs={'path': self.path.strip('/')})
    
    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.title)
        self.path = f'/{self.slug.strip('/')}'
        self.route_name = 'app.modules.pages:pages.home' if self.is_home else 'app.modules.pages:pages.' + str(self.id)
        super().save(*args, **kwargs)
