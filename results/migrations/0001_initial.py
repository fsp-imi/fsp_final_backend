# Generated by Django 5.1.3 on 2024-12-07 06:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0004_alter_agegroup_end'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='Очки')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contest_results', to='contests.contest', verbose_name='Соревнование')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_results', to='contests.contest', verbose_name='Участник')),
            ],
        ),
    ]
