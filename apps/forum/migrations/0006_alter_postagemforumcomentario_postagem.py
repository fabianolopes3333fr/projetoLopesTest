# Generated by Django 5.0.6 on 2024-07-12 18:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_postagemforumcomentario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postagemforumcomentario',
            name='postagem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postagem_comentario', to='forum.postagemforum'),
        ),
    ]
