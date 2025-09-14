from django.shortcuts import render
from .presenter import MessagePresenter

class HelloView:
    def display(self, message, request):
        return render(request, 'hello/index.html', {'message': message.text})


def index(request):
    view = HelloView()
    presenter = MessagePresenter(view)
    # pass the request to render inside Presenter
    return presenter.show_hello(request)
