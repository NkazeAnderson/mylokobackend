# Generated by Django 5.0.3 on 2024-03-21 21:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Properties', '0005_alter_property_amenities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads')),
                ('is_primary', models.BooleanField(default=False)),
                ('is_video', models.BooleanField(default=False)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.property')),
            ],
        ),
    ]
