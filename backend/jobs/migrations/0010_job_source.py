# Generated by Django 5.1.2 on 2024-11-17 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_alter_job_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='source',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
