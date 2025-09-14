from .models import Message

class MessagePresenter:
    def __init__(self, view):
        self.view = view

    def show_hello(self, request):
        message, _ = Message.objects.get_or_create(text="Abdul Awal Nadim")
        return self.view.display(message, request)
