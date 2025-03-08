from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm  

from .forms import UserRegisterForm, CourseForm, EnrollmentForm
from .models import Course, UserProfile
from .serializers import CourseSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # Redirect to home after login
    else:
        form = UserRegisterForm()
    
    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("course-list-html")  # Make sure 'home' is the correct URL name

    else:
        form = AuthenticationForm()
        
    return render(request, "login.html", {"form": form})

def course_list_html(request):
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})

@api_view(['GET', 'POST'])
def course_list_api(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("course-list-html")  # Redirect to course listing
    else:
        form = CourseForm()
    
    return render(request, "add_course.html", {"form": form})

def enroll_course(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            course = form.cleaned_data['course']
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.enrolled_courses.add(course)
            return redirect('course-list-html')  # Redirect to courses page
    else:
        form = EnrollmentForm()

    return render(request, 'enroll.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Ensure UserProfile is only created if it doesn't exist
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("home")  # Redirect to home after login
    else:
        form = UserRegisterForm()
    
    return render(request, "register.html", {"form": form})
