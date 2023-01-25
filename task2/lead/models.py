from __future__ import annotations
from enum import Enum

from django.db import models
from django.dispatch import Signal

from .core.senders import Sender

custom_post_save = Signal()


class LeadState(models.Model):
    # pk экземпляров модели
    class States(Enum):
        STATE_NEW = 1  # Новый
        STATE_IN_PROGRESS = 2  # В работе
        STATE_POSTPONED = 3  # Приостановлен
        STATE_DONE = 4  # Завершен

    name = models.CharField(
        u"Название",
        max_length=50,
        unique=True,)


class Lead(models.Model):
    name = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name=u"Имя")

    state = models.ForeignKey(
        LeadState,
        on_delete=models.PROTECT,
        default=LeadState.States.STATE_NEW.value,
        verbose_name=u"Состояние",)

    #  Не лучшее место для таких методов здесь, но по условию задачи обработчики должны быть в классе модели
    @staticmethod
    def handle_new_to_in_progress(instance: Lead):
        instance.name = 'POOR IMAGINATION'

    @staticmethod
    def handle_in_progress_to_postponed(instance: Lead, notifier: Sender):
        notifier.send(message=instance.pk)

    @staticmethod
    def handle_in_progress_to_done(instance: Lead):
        instance.name = 'POORER IMAGINATION'

    @staticmethod
    def handle_postponed_to_in_progress(instance: Lead, notifier: Sender):
        notifier.send(message=instance.pk)

    @staticmethod
    def handle_postponed_to_done(instance: Lead):
        instance.name = 'THE POOREST IMAGINATION'

    def save(self, *args, notify_by: Sender = None, **kwargs):
        if notify_by:
            custom_signal_kwargs = {
                "sender": self.__class__,
                "instance": self,
                "created": self.pk is None,
                "notifier": notify_by
            }

            custom_post_save.send(**custom_signal_kwargs)

        super().save(*args, **kwargs)

from . import signals
