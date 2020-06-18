from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect, Http404,redirect
from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib import messages
from django.forms.models import modelformset_factory
from django.conf.urls import url
from django.urls import reverse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from home.models import UserProfile,Question,Answer,Notification
from home.forms import QuestionForm,UserProfileForm,AnswerForm

def LoginPage(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('UserProfile')

        else:
            return redirect('login')

    else:

        context = locals()

        return render(request,'login.html',context)


def RegisterPage(request):


    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:

            if User.objects.filter(username=username).exists():
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                return redirect('register')

            user1 = User.objects.create_user(username=username,email=email,password=password)
            user1.save()
            friend , created = UserProfile.objects.get_or_create(user=user1,prof_pic='static/social.png',level='Beginner')

            return redirect('login')

        else:
            return redirect('register')

    else:

        context = locals()

        return render(request,'register.html',context)


def UserSettings(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count


    context = { "count_notis":total_Notis,'u1':users1 }
    return render(request,'UserSettings.html',context)

def Logout(request):

    auth.logout(request)
    return redirect('login')


def ProfileSettings(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    myprofileForm = UserProfileForm(request.POST or None, request.FILES or None , instance=users1 )
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    if myprofileForm.is_valid():
        myprofileForm.save()
        return redirect('UserProfile')

    context = { "count_notis":total_Notis,'form':myprofileForm,'u1':users1 }
    return render(request,'ProfileSettings.html',context)


def allUsers(request):

    users1 = UserProfile.objects.exclude(user=request.user).all()
    users2 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    return render(request,'allUsers.html',{'all_users':users1,"count_notis":total_Notis})


def AskQuestion(request):

    myquestionForm = QuestionForm(request.POST or None,  request.FILES or None )
    users1 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    if myquestionForm.is_valid():

        myquestionForm.instance.user = request.user
        myquestionForm.save()
 
        q_id = myquestionForm.instance.id

        qs = Question.objects.get(id=q_id)

        for q in UserProfile.objects.filter(user=request.user):
            q.Questions.add(qs)


            for usr in UserProfile.objects.exclude(user=request.user).all():

                for foll in usr.following.all():

                    if foll == users1:
                        notis , created = Notification.objects.get_or_create(user=usr,from_user=users1,message="had asked a Question",Question_id=q_id)

        return redirect('myQuestion')

    context = { 'form':myquestionForm,"count_notis":total_Notis }
    return render(request,'AskQuestion.html',context)


def UpdateQuestion(request,pk):

    users2 = UserProfile.objects.filter(user=request.user).first()
    qss1 = Question.objects.get(id=pk)
    myquestionForm = QuestionForm(request.POST or None, request.FILES or None, instance=qss1 )
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    if myquestionForm.is_valid():
        myquestionForm.save()
 
        q_id = myquestionForm.instance.id

        qs = Question.objects.get(id=q_id)

        for usr in UserProfile.objects.exclude(user=request.user).all():

            for foll in usr.following.all():

                if foll == qss1.user:
                    notis , created = Notification.objects.get_or_create(user=usr,from_user=qss1.user,message="had updated his Question",Question_id=q_id)

        return redirect('myQuestion')

    context = { 'form':myquestionForm,"count_notis":total_Notis }
    return render(request,'AskQuestion.html',context)


def DeleteQuestion(request,pk):

    qss1 = Question.objects.get(id=pk)
    qss1.delete()

    Notis = Notification.objects.filter(Question_id=pk)
    Notis.delete()

    return redirect('myQuestion')



def UpdateProfile(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    return render(request,'UserProfile1.html',{'UP':users1,"count_notis":total_Notis })


def UserProfile1(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    all_ans = Answer.objects.filter(user=users1).all().count
    all_users = UserProfile.objects.filter().all()
    qs = Question.objects.filter(user=request.user).all().count
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count
    ans = Answer.objects.filter(user=users1).all()
    fav_ans = users1.FavAnswers.all().count()
    fav_qs = users1.FavQuestions.all().count()

    users = []

    for qns in users1.Questions.all():

        for n in all_users:

            for qns1 in n.FavQuestions.all():
            
                if qns1 == qns:

                    users.append(qns1)

    
    mylist = list(dict.fromkeys(users))
    m1 = len(users)

    counts = 0
    for items in range(len(mylist)):
        counts += 1


    usersFA = []

    for ans1 in ans:

        for n in all_users:

            for qns1 in n.FavAnswers.all():
            
                if qns1 == ans1:

                    usersFA.append(qns1)

    mylist2 = list(dict.fromkeys(usersFA))

    counts1 = 0
    for items in range(len(mylist2)):
        counts1 += 1


    context = {'UP':users1,'answers':all_ans,'qs':qs,
                "count_notis":total_Notis,'fav_ans':fav_ans,
                'fav_qs':fav_qs,'b_qs':counts,'b_ans':counts1}

    return render(request,'UserProfile1.html',context)


def DetailAnswer(request,pk):

    qs = Answer.objects.filter(id=pk).first()
    total_ans = Answer.objects.filter(question=qs).all().count
    users1 = UserProfile.objects.filter(user=request.user).first()

    if UserProfile.objects.filter(user=request.user,FavAnswers=qs).exists():
        condition = "True"
    else:
        condition = "False"

    condition1 = "False"
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    context1 = {'aq':qs,'curr_user':users1,'cond':condition,'cond1':condition1,
                "count_notis":total_Notis,'total_ans':total_ans }

    return render(request,'DetailAnswer.html',context1)

def DetailQuestion(request,pk):

    qs = Question.objects.get(id=pk)
    user_q = UserProfile.objects.filter(user=qs.user).first()
    total_ans = Answer.objects.filter(question=qs).all().count
    users1 = UserProfile.objects.filter(user=request.user).first()

    if UserProfile.objects.filter(user=request.user,FavQuestions=qs).exists():
        condition = "True"
    else:
        condition = "False"

    if UserProfile.objects.filter(user=request.user,Questions=qs).exists():
        value = 'T'
    else:
        value = 'F'    

    qs.views += 1
    qs.save()

    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count
    context1 = {'aq':qs,'user_q':user_q,'curr_user':users1,'val':value,
                'cond':condition,"count_notis":total_Notis,'total_ans':total_ans}

    return render(request,'DetailQuestion.html',context1)


def FavAnswer(request,pk):

    qs = Answer.objects.filter(id=pk).first()
    users1 = UserProfile.objects.filter(user=request.user).first()
    users2 = UserProfile.objects.filter(user=qs.user.user).first()
    q_id = qs.id

    for q in UserProfile.objects.filter(user=request.user):
        q.FavAnswers.add(qs)

        if users2.user != request.user:
            notis , created = Notification.objects.get_or_create(user=users2,from_user=users1,message="Liked Your Answer",Question_id=q_id)

    return redirect('DetailAnswer',pk=pk)


def FavQuestion(request,pk):

    qs = Question.objects.filter(id=pk).first()
    users1 = UserProfile.objects.filter(user=request.user).first()
    users2 = UserProfile.objects.filter(user=qs.user).first()
    q_id = qs.id

    for q in UserProfile.objects.filter(user=request.user):
        q.FavQuestions.add(qs)

        if users2.user != request.user:
            notis , created = Notification.objects.get_or_create(user=users2,from_user=users1,message="Liked Your Question",Question_id=q_id)

    return redirect('DetailQuestion',pk=pk)


def UserFavAnswer(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    context = { 'qs':users1,"count_notis":total_Notis }
    return render(request,'FavAns.html',context)


def DetailAnswer(request,pk):

    qs = Answer.objects.filter(id=pk).first()
    users1 = UserProfile.objects.filter(user=request.user).first()
    users2 = UserProfile.objects.filter(user=qs.user.user).first()
    q_id = qs.id

    if UserProfile.objects.filter(user=request.user,FavAnswers=qs).exists():
        condition = "True"
    else:
        condition = "False"

    context = {'ans':qs,'cond':condition}

    return render(request,'DetailAns.html',context)


def FollowUser(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    curr_User = UserProfile.objects.filter(user=request.user).first()

    ans = Answer.objects.filter(user=users1).all().count
    qs = Question.objects.filter(user=users1.user).all().count


    for q in UserProfile.objects.filter(user=request.user):

        q.following.add(users1)

    for q1 in UserProfile.objects.filter(id=pk):

        q1.followers.add(curr_User)
        
        notis , created = Notification.objects.get_or_create(user=users1,from_user=curr_User,message="had started Following You")

    return redirect('DetailProfile',pk=pk)


def DetailProfile(request,pk):

    users1 = UserProfile.objects.get(id=pk)
    curr_User = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=curr_User,viewed=False).all().count
    all_ans = Answer.objects.filter(user=users1).all().count
    ans = Answer.objects.filter(user=users1).all()
    qs = Question.objects.filter(user=users1.user).all().count
    all_users = UserProfile.objects.filter().all()
    fav_ans = users1.FavAnswers.all().count()
    fav_qs = users1.FavQuestions.all().count()


    if UserProfile.objects.filter(user=request.user,following=users1).exists():
        condition = "True"
    else:
        condition = "False"

    users = []

    for qns in users1.Questions.all():

        for n in all_users:

            for qns1 in n.FavQuestions.all():
            
                if qns1 == qns:

                    users.append(qns1)

    
    mylist = list(dict.fromkeys(users))
    m1 = len(users)

    counts = 0
    for items in range(len(mylist)):
        counts += 1


    usersFA = []

    for ans1 in ans:

        for n in all_users:

            for qns1 in n.FavAnswers.all():
            
                if qns1 == ans1:

                    usersFA.append(qns1)

    mylist2 = list(dict.fromkeys(usersFA))

    counts1 = 0
    for items in range(len(mylist2)):
        counts1 += 1


    context = {'UP':users1,'answers':all_ans,'qs':qs,
                'Curr_User':curr_User,'cond':condition,
                "count_notis":total_Notis,'fav_ans':fav_ans,
                'fav_qs':fav_qs,'b_qs':counts,'b_ans':counts1}

    return render(request,'UserProfile1.html',context)


def ShowAnswer(request,pk):
    
    users1 = Question.objects.get(id=pk)
    ans = Answer.objects.filter(question=users1).all()
    profile = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=profile,viewed=False).all().count

    if UserProfile.objects.filter(user=request.user,FavQuestions=users1).exists():
        condition = "True"
    else:
        condition = "False"


    context = { 'ans':ans,'qs':users1,"count_notis":total_Notis,
                'profile':profile,'cond':condition}

    return render(request,'ShowAnswer.html',context)


def AnswerQuestions(request,pk):

    qs1 = Question.objects.get(id=pk)
    profile = UserProfile.objects.filter(user=request.user).first()
    profile1 = UserProfile.objects.filter(user=qs1.user).first()
    total_Notis = Notification.objects.filter(user=profile,viewed=False).all().count
    q_id = qs1.id

    myAnsForm = AnswerForm(request.POST or None)

    if myAnsForm.is_valid():

        myAnsForm.instance.user = profile
        myAnsForm.instance.question = qs1
        myAnsForm.instance.questioner = profile1
        myAnsForm.save()

        qs1.answers += 1
        qs1.save()

        if profile1.user != request.user:
            notis , created = Notification.objects.get_or_create(user=profile1,from_user=profile,message="had answered your question",Question_id=q_id)

        return redirect('myQuestion')

    context = { 'form':myAnsForm,"count_notis":total_Notis}
    return render(request,'AnswerQ.html',context)


def UpdateAnswer(request,pk):

    qs1 = Answer.objects.get(id=pk)
    profile = UserProfile.objects.filter(user=request.user).first()
    profile1 = UserProfile.objects.filter(user=qs1.user.user).first()
    total_Notis = Notification.objects.filter(user=profile,viewed=False).all().count
    q_id = qs1.id

    myAnsForm = AnswerForm(request.POST or None,instance=qs1)

    if myAnsForm.is_valid():
        myAnsForm.save()

        if profile1.user != request.user:
            notis , created = Notification.objects.get_or_create(user=profile1,from_user=profile,message="had updated his Aswer",Question_id=q_id)

        return redirect('UserAnswers')

    context = { 'form':myAnsForm,"count_notis":total_Notis}
    return render(request,'AnswerQ.html',context)


def DeleteAns(request,pk):

    ans = Answer.objects.get(id=pk)
    ans.delete()

    Notis = Notification.objects.filter(Question_id=pk)
    Notis.delete()

    return redirect('UserAnswers')


def UserAnswers(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    users2 = UserProfile.objects.filter(user=request.user).first()
    ans = Answer.objects.filter(user=users1).all()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    context = { 'ans':ans,'UP':users1,"count_notis":total_Notis}
    return render(request,'UserAns.html',context)

def myQuestion(request):

    users1 = UserProfile.objects.filter().all()
    c_user = UserProfile.objects.filter(user=request.user).first()
    count_fav = c_user.FavQuestions.all().count
    total_Notis = Notification.objects.filter(user=c_user,viewed=False).all().count


    for us in users1:
        for qns in us.Questions.all():

            if UserProfile.objects.filter(user=request.user,FavQuestions=qns).exists():
                qns.fav = "True"
            else:
                qns.fav = "False"

    context = {'all_qs':users1,'curr_user':c_user,'count_fav':count_fav,"count_notis":total_Notis}
    return render(request,'Question.html',context)


def UserFavQuestions(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    qs = Answer.objects.filter(questioner=users1).all()
    users2 = UserProfile.objects.filter().all()
    users3 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users3,viewed=False).all().count

    context = { 'qs':users1, 'an':qs,"count_notis":total_Notis,'u2':users2 }
    return render(request,'FavQs.html',context)


def UserQuestions(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    qs = Answer.objects.filter(questioner=users1).all()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    context = { 'qs':users1, 'an':qs,"count_notis":total_Notis }
    return render(request,'UserQs.html',context)

def UserBestQuestions(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    users2 = UserProfile.objects.filter(user=request.user).first()
    all_users = UserProfile.objects.filter().all()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    users = []

    for qns in users1.Questions.all():

        for n in all_users:

            for qns1 in n.FavQuestions.all():
            
                if qns1 == qns:

                    users.append(qns1)

    mylist = list(dict.fromkeys(users))

    context = { 'qs':mylist,'u1':users1 }

    return render(request,'UserBestQs1.html',context)


def UserBestAnswer(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    users2 = UserProfile.objects.filter(user=request.user).first()
    all_users = UserProfile.objects.filter().all()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count
    ans = Answer.objects.filter(user=users1).all()

    users = []

    for ans1 in ans:

        for n in all_users:

            for qns1 in n.FavAnswers.all():
            
                if qns1 == ans1:

                    users.append(qns1)

    mylist = list(dict.fromkeys(users))

    print(mylist.count)

    context = { 'qs':mylist,'u1':users1 }

    return render(request,'UserBestAns1.html',context)


def OtherUserQuestions(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    qs = Answer.objects.filter(questioner=users1).all()
    users2 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    context = { 'qs':users1, 'an':qs,"count_notis":total_Notis }
    return render(request,'UserQs.html',context)


def UserFollowers(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    context = { 'curr_user':users1,"count_notis":total_Notis }
    return render(request,'UserFollowers.html',context)

def OtherUserFollowers(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    users2 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    context = { 'curr_user':users1,"count_notis":total_Notis }
    return render(request,'UserFollowers.html',context)


def OtherUserFollowing(request,pk):

    users1 = UserProfile.objects.filter(id=pk).first()
    users2 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users2,viewed=False).all().count

    context = { 'curr_user':users1 ,"count_notis":total_Notis }
    return render(request,'UserFollowing.html',context)


def UserNotifications(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    Notis = Notification.objects.filter(user=users1).all().order_by('-dateTime').order_by('viewed')
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    context = { 'my_notis':Notis,"count_notis":total_Notis }
    return render(request,'UserNotifications.html',context)

def ReadNotifs(request,pk):

    Notis = Notification.objects.filter(id=pk).first()
    Notis.viewed = True
    Notis.save()
    return redirect('UserNotifications')


def UserFollowing(request):

    users1 = UserProfile.objects.filter(user=request.user).first()
    total_Notis = Notification.objects.filter(user=users1,viewed=False).all().count

    context = { 'curr_user':users1,"count_notis":total_Notis }

    return render(request,'UserFollowing.html',context)
