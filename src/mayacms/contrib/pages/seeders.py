from django.apps.registry import Apps


def type_seeder(apps: Apps, schema_editor):
    Type = apps.get_model('pages', 'Type')
    Type.objects.create(
        name = 'Default',
        slug = 'default',
        description = 'An example page type.',
    )

def page_seeder(apps: Apps, schema_editor):
    Type = apps.get_model('pages', 'Type')
    Page = apps.get_model('pages', 'Page')

    Page.objects.create(
        title = 'Home',
        slug = 'home',
        path = '/home',
        route_name = 'mayacms.contrib.pages:pages.home',
        content = 'Welcome to MayaCMS!',
        is_enabled = True,
        is_home = True,
        type = Type.objects.get(slug='default'),
    )

    Page.objects.create(
        title = 'Contact',
        slug = 'contact',
        path = '/contact',
        route_name = 'mayacms.contrib.pages:pages.contact',
        content = 'Contact Us',
        is_enabled = True,
        is_home = False,
        type = Type.objects.get(slug='default'),
    )
