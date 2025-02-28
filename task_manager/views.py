from django.http import HttpResponse


def index(request):
    return HttpResponse("Добро пожаловать на мой сайт!")
