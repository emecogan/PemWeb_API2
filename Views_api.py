#viewsapi
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from MyProject.models import (Course)
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json,requests



@csrf_exempt
def apiCourse(request):
    if request.method == "GET":
        data = serializers.serialize("json", Course.objects.all())
        return JsonResponse(json.loads(data), safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            created = Course.objects.create(course_name=body['course_name'])
            return JsonResponse({"message": "data successfully created!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"message": "data is not json type!"}, status=400)
        except KeyError:
            return JsonResponse({"message": "missing required field: course_name"}, status=400)

    elif request.method == "PUT":
        try:
            body = json.loads(request.body.decode("utf-8"))
            course = Course.objects.get(id=body['id'])
            course.course_name = body['course_name']
            course.save()
            return JsonResponse({"message": "data successfully updated!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message": "data is not json type!"}, status=400)
        except KeyError:
            return JsonResponse({"message": "missing required field: id or course_name"}, status=400)
        except Course.DoesNotExist:
            return JsonResponse({"message": "course not found!"}, status=404)

    elif request.method == "DELETE":
        try:
            body = json.loads(request.body.decode("utf-8"))
            course = Course.objects.get(id=body['id'])
            course.delete()
            return JsonResponse({"message": "data successfully deleted!"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"message": "data is not json type!"}, status=400)
        except KeyError:
            return JsonResponse({"message": "missing required field: id"}, status=400)
        except Course.DoesNotExist:
            return JsonResponse({"message": "course not found!"}, status=404)

    return HttpResponse(status=405)


@csrf_exempt
def consumeApiGet(request):
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    data = response.json()
    return render(request, "api-get.html", {'data': data})
