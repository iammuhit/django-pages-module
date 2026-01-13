from django.db import migrations
from mayacms.contrib.pages import seeders


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seeders.type_seeder),
        migrations.RunPython(seeders.page_seeder),
    ]
