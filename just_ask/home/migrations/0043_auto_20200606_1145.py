# Generated by Django 2.2 on 2020-06-06 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0042_answer_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='tag',
            field=models.CharField(default='-', max_length=20),
        ),
    ]
