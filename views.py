import sys
from django.contrib import messages
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.contrib.auth.models import User
from MyProject.models import AccountUser, Course, AttendingCourse
from MyProject.signals import check_nim
from MyProject.forms import StudentRegisterForm

# Create your views here.
def home(request):
    #fungsi (def) nama fungsinya(home)
    return render(request, 'home.html')


def readCourse(request):
    data = Course.objects.all()[:1]  # limit data (1 pcs)
    context = {'data_list': data}
    return render(request, 'course.html', context)


@csrf_protect
def createCourse(request):
    if request.method == 'POST':
        # Logika untuk membuat course baru
        pass
    return render(request, 'home.html')


@csrf_protect
def updateCourse(request):
    if request.method == 'POST':
        # Logika untuk mengupdate course
        pass
    return render(request, 'home.html')


@csrf_protect
def deleteCourse(request, id):
    try:
        data = Course.objects.filter(course_id=id)
        if data:
            data.delete()
            messages.success(request, 'Data Berhasil dihapus')
        else:
            messages.success(request, 'Data Tidak ditemukan')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('MyProject:read-data-course')


def readStudent(request):
    data = AccountUser.objects.all()
    context = {'data_list': data}
    return render(request, 'index.html', context)


@csrf_protect
def createStudent(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            post_save.disconnect(check_nim, sender=AccountUser, dispatch_uid="check_nim")
            new_student = form.save(commit=False)
            new_student.fullname = form.cleaned_data.get("fullname")
            new_student.nim = form.cleaned_data.get("nim")
            new_student.email = form.cleaned_data.get("email")
            new_student.save()
            post_save.connect(check_nim, sender=AccountUser, dispatch_uid="check_nim")
            messages.success(request, 'Data Berhasil disimpan')
            return redirect('MyProject:read-data-student')
    else:
        form = StudentRegisterForm()
    return render(request, 'form.html', {'form': form})


@csrf_protect
def updateStudent(request, id):
    if request.method == 'POST':
        # Logika untuk mengupdate student
        messages.success(request, 'Data Berhasil disimpan')
        return redirect('MyProject:read-data-student')
    return render(request, 'form.html')


@csrf_protect
def deleteStudent(request, id):
    try:
        member = AccountUser.objects.get(account_user_related_user=id)
        user = User.objects.get(username=id)
        member.delete()
        user.delete()
        messages.success(request, 'Data Berhasil dihapus')
    except Exception as e:
        messages.error(request, f'Error: {e}')
    return redirect('MyProject:read-data-student')


# Create API with Methods PUT & DELETE

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from MyProject.serializers import CourseSerializer, AccountUserSerializer

@api_view(['PUT'])
def update_course_api(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_course_api(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
