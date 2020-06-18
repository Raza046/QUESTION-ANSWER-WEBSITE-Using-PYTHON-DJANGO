from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('login', views.LoginPage, name="login"),
    path('logout', views.Logout, name="logout"),
    path('register', views.RegisterPage, name="register"),
    path('allUser', views.allUsers, name="allUser"),
    path('UserProfile', views.UserProfile1, name="UserProfile"),
    path('AnsQuestion <str:pk>', views.AnswerQuestions, name="AnsQuestion"),
    path('myQuestion', views.myQuestion, name="myQuestion"),
    path('DetailProfile <str:pk>', views.DetailProfile, name="DetailProfile"),
    path('ShowAnswer <str:pk>', views.ShowAnswer, name="ShowAnswer"),
    path('FollowUser <str:pk>', views.FollowUser, name="FollowUser"),
    path('FavQuestion <str:pk>', views.FavQuestion, name="FavQuestion"),
    path('AskQuestion', views.AskQuestion, name="AskQuestion"),
    path('UserAnswers <str:pk>', views.UserAnswers, name="UserAnswers"),
    path('UserFollowers', views.UserFollowers, name="UserFollowers"),
    path('UserQuestions', views.UserQuestions, name="UserQuestions"),
    path('UserBestQuestions <str:pk>', views.UserBestQuestions, name="UserBestQuestions"),
    path('UserBestAnswer <str:pk>', views.UserBestAnswer, name="UserBestAnswer"),
    path('UserFollowing', views.UserFollowing, name="UserFollowing"),
    path('UserFavQuestions <str:pk>', views.UserFavQuestions, name="UserFavQuestions"),
    path('FavAnswer <str:pk>', views.FavAnswer, name="FavAnswer"),    
    path('UserFavAnswer <str:pk>', views.UserFavAnswer, name="UserFavAnswer"),    
    path('DetailAnswer <str:pk>', views.DetailAnswer, name="DetailAnswer"),
    path('DetailQuestion <str:pk>', views.DetailQuestion, name="DetailQuestion"),
    path('OUserQuestions <str:pk>', views.OtherUserQuestions, name="OUserQuestions"),
    path('OtherUserFollowing <str:pk>', views.OtherUserFollowing, name="OtherUserFollowing"),
    path('OtherUserFollower <str:pk>', views.OtherUserFollowers, name="OtherUserFollower"),
    path('OtherUserBestQuest <str:pk>', views.UserBestQuestions, name="OtherUserBestQuest"),
    path('UserNotifications', views.UserNotifications, name="UserNotifications"),
    path('UserSettings', views.UserSettings, name="UserSettings"),
    path('ProfileSettings <str:pk>', views.ProfileSettings, name="ProfileSettings"),
    path('UpdateQuestion <str:pk>', views.UpdateQuestion, name="UpdateQuestion"),
    path('DeleteQuestion <str:pk>', views.DeleteQuestion, name="DeleteQuestion"),
    path('ReadNotifs <str:pk>', views.ReadNotifs, name="ReadNotifs"),
    path('UpdateAnswer <str:pk>', views.UpdateAnswer, name="UpdateAnswer"),
    path('DeleteAns <str:pk>', views.DeleteAns, name="DeleteAns"),


]
