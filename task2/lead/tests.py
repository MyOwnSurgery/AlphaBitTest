from django.test import TestCase

# Create your tests here.
from .models import Lead, LeadState
from .core.senders import SMSSender, EmailSender


class StateTransitionTest(TestCase):
    def setUp(self):
        LeadState.objects.create(pk=1, name='NEW')  # Пусть будет явно
        LeadState.objects.create(pk=2, name='IN_PROGRESS')
        LeadState.objects.create(pk=3, name='POSTPONED')
        LeadState.objects.create(pk=4, name='DONE')

        Lead.objects.create(name="NEW")
        Lead.objects.create(name="IN_PROGRESS_FIRST", state=LeadState.objects.get(name='IN_PROGRESS'))
        Lead.objects.create(name="IN_PROGRESS_SECOND", state=LeadState.objects.get(name='IN_PROGRESS'))
        Lead.objects.create(name="POSTPONED_FIRST", state=LeadState.objects.get(name='POSTPONED'))
        Lead.objects.create(name="POSTPONED_SECOND", state=LeadState.objects.get(name='POSTPONED'))

    def test_new_to_in_progress_transition_handling(self):
        lead = Lead.objects.get(name="NEW")
        lead.state = LeadState.objects.get(name='IN_PROGRESS')
        lead.save()

        self.assertEqual(Lead.objects.get(pk=lead.pk).name, 'POOR IMAGINATION')

    def test_in_progress_to_done_transition_handling(self):
        lead = Lead.objects.get(name="IN_PROGRESS_FIRST")
        lead.state = LeadState.objects.get(name='DONE')
        lead.save()

        self.assertEqual(Lead.objects.get(pk=lead.pk).name, 'POORER IMAGINATION')

    def test_postponed_to_done_transition_handling(self):
        lead = Lead.objects.get(name="POSTPONED_FIRST")
        lead.state = LeadState.objects.get(name='DONE')
        lead.save()

        self.assertEqual(Lead.objects.get(pk=lead.pk).name, 'THE POOREST IMAGINATION')

    def test_in_progress_to_postponed_transition_handling(self):
        lead = Lead.objects.get(name="IN_PROGRESS_SECOND")
        lead.state = LeadState.objects.get(name='POSTPONED')

        sender = SMSSender()
        lead.save(notify_by=sender)

        self.assertEqual(sender.number_of_calls, 1)

    def test_postponed_to_in_progress_transition_handling(self):
        lead = Lead.objects.get(name="IN_PROGRESS_SECOND")
        lead.state = LeadState.objects.get(name='POSTPONED')

        sender = EmailSender()
        lead.save(notify_by=sender)

        self.assertEqual(sender.number_of_calls, 1)
