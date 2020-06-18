from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

showChoices = (

    ('Beginner' , 'Beginner'),
    ('Intermediate' , 'Intermediate'),
    ('advance' , 'advance'),
)

ReportChoices = (

    ('Invalid-content','Invalid-content'),

)


FavChoices = (

    ('Yes','Yes'),
    ('No','No')
)



class Question(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    q_image = models.ImageField(upload_to='static',null=True)
    q_title = models.CharField(max_length=100)
    tag = models.CharField(max_length=20)
    content = models.TextField()
    answers = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    fav = models.CharField(max_length=50)
    report = models.CharField(choices=ReportChoices,max_length=50)
    dateTime = models.DateTimeField(auto_now=True)
     

class UserProfile(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    prof_pic = models.ImageField(upload_to='static')
    level = models.CharField(choices=showChoices,max_length=50)
    followers = models.ManyToManyField('self',related_name='follow',null=True)
    following = models.ManyToManyField('self',related_name='followings',null=True)
    Questions = models.ManyToManyField(Question,null=True)
    FavQuestions = models.ManyToManyField(Question,related_name='FavQuestion',null=True)
    FavAnswers = models.ManyToManyField("Answer",related_name='FavAnswer',null=True)


class Answer(models.Model):

    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    questioner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='questioner')
    question = models.ForeignKey(Question,on_delete=models.CASCADE,null=True)
    content = models.TextField()
    tag = models.CharField(max_length=20)
    dateTime = models.DateTimeField(auto_now=True)


class Notification(models.Model):

    message = models.TextField()
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    from_user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='from_User')
    viewed = models.BooleanField(default=False)
    Question_id = models.CharField(max_length=50)
    dateTime = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.user.username

    def __str1__(self):
        return self.from_user.user.username
