from enum import Enum
from functools import partialmethod

from django.db import models


# Сделаем базовый абстрактный класс модели, при наследовании от которого он будет конфигурировать наследников
class AutoMethodsModel(models.Model):
    def __init_subclass__(cls, **_):
        if hasattr(cls, '_METHOD_NAME_2_PROXY_METHOD'):  # Тут бы еще проверки какие-нибудь...
            for method_name, proxy_method in cls._METHOD_NAME_2_PROXY_METHOD.items():
                setattr(cls, method_name, proxy_method)  # Добавляем прямо в класс, даже биндить не надо ничего

    class Meta:
        abstract = True


class DeliveryState(AutoMethodsModel):

    class Meta:
        verbose_name = u"Состояние доставки"
        verbose_name_plural = u"Состояния доставок"

    class _States(Enum):
        NEW = 1  # Новая
        ISSUED = 2  # Выдана курьеру
        DELIVERED = 3  # Доставлена
        HANDED = 4  # Курьер сдал
        REFUSED = 5  # Отказ
        PAID_REFUSED = 6  # Отказ с оплатой курьеру
        COMPLETE = 7  # Завершена
        NONE = 8  # Не определено

    @classmethod
    def _get_by_state(cls, state: _States):
        return cls.objects.get(pk=state.value)

    _METHOD_NAME_2_PROXY_METHOD = {
        # В принципе, можно даже не делать dict, а парсить по названию метода, но это совсем уж имплицитно
        'get_new': partialmethod(_get_by_state, _States.NEW),  # Не вызываем, просто билдим (Паттерн builder?)
        'get_issued': partialmethod(_get_by_state, _States.ISSUED),
        'get_delivered': partialmethod(_get_by_state, _States.DELIVERED),
        'get_handed': partialmethod(_get_by_state, _States.HANDED),
        'get_refused': partialmethod(_get_by_state, _States.REFUSED),
        'get_paid_refused': partialmethod(_get_by_state, _States.PAID_REFUSED),
        'get_complete': partialmethod(_get_by_state, _States.COMPLETE),
        'get_none': partialmethod(_get_by_state, _States.NONE)
    }


# Еще была идея сделать через переопределение __getattr__ у метакласса BaseModel,
# но джанговская магия не пропустила такую идею
