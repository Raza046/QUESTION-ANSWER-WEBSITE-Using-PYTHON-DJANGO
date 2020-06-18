from django import forms
from home.models import UserProfile,Question,Answer

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [ 
            'prof_pic'
         ]


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question 

        fields = [ 
            'q_title',
            'q_image',
            'tag',
            'content'
         ]

class AnswerForm(forms.ModelForm):

    class Meta:
        model =  Answer

        fields = [ 
            'content',
            'tag',

        ]


