from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    class Category(models.TextChoices):
        CARDIO_MACHINE = ("C", "Cardio machine")
        RESISTANCE_MACHINE = ("R", "Resistance machine")
        FREE_WEIGHTS = ("F", "Free weights")
        OTHER = ("O", "Other")

    category = models.CharField(max_length=1, choices=Category.choices, default=Category.CARDIO_MACHINE)

    weight_measured = models.BooleanField(default=False, verbose_name="Is this exercise measured by weight?")
    reps_measured = models.BooleanField(default=False, verbose_name="Is this exercise measured by number of repetitions?")
    duration_measured = models.BooleanField(default=False, verbose_name="Is this exercise measured by its duration?")
    distance_measured = models.BooleanField(default=False, verbose_name="Is this exercise measured by distance?")
    difficulty_level_measured = models.BooleanField(default=False, verbose_name="Is this exercise measured by difficulty level?")
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Workout(models.Model):
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, verbose_name="Weight kg)")
    
    class Meta:
        ordering = ["start_dt"]

    def __str__(self):
        return f"Workout on {self.start_dt.date().strftime('%d-%m-%Y')}"
    

class WorkoutExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.deletion.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.deletion.CASCADE)
    sets = models.IntegerField(default=1)
    weight = models.FloatField(null=True, blank=True, verbose_name="Weight (kgs)")
    reps = models.IntegerField(null=True, blank=True, verbose_name="Repetitions")
    duration = models.DurationField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True, verbose_name="Distance (metres)")
    difficulty_level = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["workout__start_dt", "exercise__category", "exercise__name"]

    def __str__(self):
        return f"{self.exercise.name} on {self.workout.start_dt.date().strftime('%d-%m-%Y')}"

