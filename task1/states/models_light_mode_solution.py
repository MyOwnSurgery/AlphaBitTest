from enum import Enum

from django.db import models


class DeliveryState(models.Model):

    class Meta:
        verbose_name = u"Состояние доставки"
        verbose_name_plural = u"Состояния доставок"

    # Можно в какой-нибудь другой модуль вынести, но пусть будет тут и protected
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

    #  Протягиваем уже существующий интерфейс, но с более удачной реализацией
    #  Теперь у нас get только в одном месте
    @classmethod
    def get_new(cls):
        return cls._get_by_state(state=cls._States.NEW)

    @classmethod
    def get_issued(cls):
        return cls._get_by_state(state=cls._States.ISSUED)

    @classmethod
    def get_delivered(cls):
        return cls._get_by_state(state=cls._States.DELIVERED)

    @classmethod
    def get_handed(cls):
        return cls._get_by_state(state=cls._States.HANDED)

    @classmethod
    def get_refused(cls):
        return cls._get_by_state(state=cls._States.REFUSED)

    @classmethod
    def get_paid_refused(cls):
        return cls._get_by_state(state=cls._States.PAID_REFUSED)

    @classmethod
    def get_complete(cls):
        return cls._get_by_state(state=cls._States.COMPLETE)

    @classmethod
    def get_none(cls):
        return cls._get_by_state(state=cls._States.NONE)
