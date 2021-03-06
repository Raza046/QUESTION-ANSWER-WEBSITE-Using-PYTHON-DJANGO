# Generated by Django 2.2 on 2020-05-14 22:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0008_question_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='Questions',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='home.Question'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='followers',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='following',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
