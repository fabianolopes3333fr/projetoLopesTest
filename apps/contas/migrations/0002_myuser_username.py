# Generated by Django 5.0.6 on 2024-06-29 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
