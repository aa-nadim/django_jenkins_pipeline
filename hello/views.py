from django.shortcuts import render
from .presenter import MessagePresenter
from django.http import JsonResponse
import json


class HelloView:
    def display(self, message, request):
        return render(request, 'hello/index.html', {'message': message.text})


def index(request):
    view = HelloView()
    presenter = MessagePresenter(view)
    # pass the request to render inside Presenter
    return presenter.show_hello(request)


def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'Django Hello World is running!',
        'version': '1.0.0'
    })