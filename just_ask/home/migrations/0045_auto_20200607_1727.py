# Generated by Django 2.2 on 2020-06-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0044_auto_20200606_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='fav',
            field=models.CharField(max_length=50),
        ),
    ]
