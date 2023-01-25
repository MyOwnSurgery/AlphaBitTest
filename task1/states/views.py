from django.http import HttpResponse
from .models import DeliveryState


#  Просто тестовые вьюхи
def get_new(_):
    return HttpResponse(DeliveryState.get_new().pk)


def get_issued(_):
    return HttpResponse(DeliveryState.get_issued().pk)


def get_delivered(_):
    return HttpResponse(DeliveryState.get_delivered().pk)


def get_handed(_):
    return HttpResponse(DeliveryState.get_handed().pk)


def get_refused(_):
    return HttpResponse(DeliveryState.get_refused().pk)


def get_paid_refused(_):
    return HttpResponse(DeliveryState.get_paid_refused().pk)


def get_complete(_):
    return HttpResponse(DeliveryState.get_complete().pk)


def get_none(_):
    return HttpResponse(DeliveryState.get_none().pk)

