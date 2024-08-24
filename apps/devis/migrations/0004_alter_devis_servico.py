# Generated by Django 5.0.6 on 2024-08-17 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devis', '0003_rename_trabalho_devis_servico_devis_data_criacao_and_more'),
        ('pages', '0006_alter_servico_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devis',
            name='servico',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.servico'),
        ),
    ]