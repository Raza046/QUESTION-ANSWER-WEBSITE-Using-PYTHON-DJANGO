# Generated by Django 2.2 on 2020-05-26 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_answer_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='FavQuestions',
            field=models.ManyToManyField(null=True, related_name='FavQuestion', to='home.Question'),
        ),
    ]