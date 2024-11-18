from .models import Exercise, WorkoutExercise

def get_enabled_metric_fields_by_exercise():
    enabled_metric_fields = {}
    for exercise in Exercise.objects.all():
        enabled_metric_fields[exercise.id] = exercise.get_enabled_metric_fields()
    return enabled_metric_fields


def get_default_metric_values_by_exercise(enabled_metric_fields_by_exercise):
    default_metric_values = {}
    for exercise_id, enabled_metric_fields in enabled_metric_fields_by_exercise.items():
        exercise_metric_values = {}
        if last_workout_exercise := WorkoutExercise.objects.filter(exercise_id=exercise_id).last():
            for metric_field in enabled_metric_fields:
                metric_value = getattr(last_workout_exercise, metric_field)
                if metric_field == "duration":
                    seconds = metric_value.seconds
                    minutes = seconds // 60
                    metric_value = f"{minutes:02}:{seconds % 60:02}"
                exercise_metric_values[metric_field] = metric_value
        default_metric_values[exercise_id] = exercise_metric_values
    return default_metric_values