# Generated by Django 5.0.3 on 2024-03-25 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Properties', '0012_alter_property_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Catergory',
            new_name='Category',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='catergory',
            new_name='category',
        ),
    ]
