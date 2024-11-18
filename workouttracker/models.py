from django.db import models
from django.templatetags.static import static

class Exercise(models.Model):
    name = models.CharField(max_length=100)

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
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.image:
            return self.image.url
        else:
            return static("workouttracker/Black square.png")
        
    @staticmethod
    def get_all_metric_fields():
        return ["weight", "reps", "duration", "distance", "difficulty_level"]
    
    def get_enabled_metric_fields(self):
        enabled_metric_fields = []
        if self.weight_measured:
            enabled_metric_fields.append("weight")
        if self.reps_measured:
            enabled_metric_fields.append("reps")
        if self.duration_measured:
            enabled_metric_fields.append("duration")
        if self.distance_measured:
            enabled_metric_fields.append("distance")
        if self.difficulty_level_measured:
            enabled_metric_fields.append("difficulty_level")
        return enabled_metric_fields



class Workout(models.Model):
    start_dt = models.DateTimeField()
    end_dt = models.DateTimeField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True, verbose_name="Weight kg)")
    
    class Meta:
        ordering = ["start_dt"]

    def __str__(self):
        return f"Workout on {self.start_dt.date().strftime('%d-%m-%Y')} at {self.start_dt.strftime("%H:%M")}"
    
    def is_complete(self):
        return bool(self.end_dt)
    

class WorkoutExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.deletion.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.deletion.CASCADE)
    weight = models.FloatField(null=True, blank=True, verbose_name="Weight (kgs)")
    reps = models.IntegerField(null=True, blank=True, verbose_name="Repetitions")
    duration = models.DurationField(null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True, verbose_name="Distance (metres)")
    difficulty_level = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(default=1)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.exercise.name} on {self.workout.start_dt.date().strftime('%d-%m-%Y')}"
    
    def get_metric_values(self):
        metric_values = {}
        for metric_field in self.exercise.get_enabled_metric_fields():
            metric_values[metric_field] = getattr(self, metric_field)
        return metric_values
