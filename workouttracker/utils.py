from .models import Exercise

def get_enabled_metric_fields_by_exercise():
    enabled_metric_fields = {}
    for exercise in Exercise.objects.all():
        enabled_metric_fields[exercise.id] = exercise.get_enabled_metric_fields()
    return enabled_metric_fields
