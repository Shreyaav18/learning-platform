from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Use the default User model
from .models import Course

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'difficulty' ]
        
class EnrollmentForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(), 
        empty_label="Select a Course"
    )


