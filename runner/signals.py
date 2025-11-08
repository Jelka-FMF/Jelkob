from django.db.models.signals import post_save
from django.dispatch import receiver
from django_eventstream import send_event

from .models import Config, Pattern, State
from .serializers import PatternSerializer, StateSerializer


@receiver(post_save, sender=Pattern)
@receiver(post_save, sender=Config)
def send_control_events(**kwargs):
    patterns = PatternSerializer(Pattern.objects.all(), many=True).data
    send_event("control", "patterns", patterns)


@receiver(post_save, sender=Pattern)
@receiver(post_save, sender=State)
@receiver(post_save, sender=Config)
def send_status_events(**kwargs):
    patterns = PatternSerializer(Pattern.objects.all(), many=True).data
    state = StateSerializer(State.get_solo()).data

    data = {"patterns": patterns, "state": state}
    send_event("status", "message", data)
