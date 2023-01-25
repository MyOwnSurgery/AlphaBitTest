from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Lead, custom_post_save
from .core.transitions import Transition, Transitions


def _get_transition_from_versions(instance: Lead):
    previous_version = Lead.objects.get(pk=instance.pk)
    state_from, state_to = previous_version.state, instance.state

    return Transition(state_from.pk, state_to.pk)


@receiver(custom_post_save, sender=Lead)
def handle_state_transition_command(sender, instance, created, notifier, **kwargs):
    """ Рассылку СМС и тд делаем в post_save """
    if created:
        return

    transition = _get_transition_from_versions(instance)

    if transition == Transitions.IN_PROGRESS_TO_POSTPONED.value:
        Lead.handle_in_progress_to_postponed(instance=instance, notifier=notifier)
    elif transition == Transitions.POSTPONED_TO_IN_PROGRESS.value:
        Lead.handle_postponed_to_in_progress(instance=instance, notifier=notifier)


@receiver(pre_save, sender=Lead)
def handle_state_transition_mutation(sender, instance, **kwargs):
    """ Необходимые сопровождающие обновления объекта модели делаем в pre_save
        Если апдейт изначально должен быть неудачный, то и это поле мы потеряем, и все останется как было """
    if instance.pk is None:  # Лучше is None, вдруг какой-нибудь id = 0 будет
        return

    transition = _get_transition_from_versions(instance)

    #  Можно было бы использовать dict в Lead и делать что-то вроде Lead.TRANSITION_2_ACTION[transition]()
    #  Но пусть будет более читаемо
    if transition == Transitions.NEW_TO_IN_PROGRESS.value:
        Lead.handle_new_to_in_progress(instance=instance)
    elif transition == Transitions.IN_PROGRESS_TO_DONE.value:
        Lead.handle_in_progress_to_done(instance=instance)
    elif transition == Transitions.POSTPONED_TO_DONE.value:
        Lead.handle_postponed_to_done(instance=instance)

    #  Вообще можно поменять значение атрибута прямо в сигнале