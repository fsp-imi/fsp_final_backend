# Generated by Django 5.1.3 on 2024-12-08 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('claims', '0012_remove_claim_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Название заявки'),
        ),
    ]