from django.http.response import HttpResponse as HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from workouttracker.templatetags.workout_extras import capitalise_and_underscore_to_space

from .forms import ExerciseForm, WorkoutEndForm, WorkoutExerciseForm
from .models import Exercise, Workout, WorkoutExercise
from .utils import get_default_metric_values_by_exercise, get_enabled_metric_fields_by_exercise

class IndexView(generic.TemplateView):
    template_name = "workouttracker/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_workout"] = Workout.objects.filter(end_dt__isnull=True).first()
        return context
    

class WorkoutStartView(generic.RedirectView):
    pattern_name = "workout"

    def get_redirect_url(self, *args, **kwargs):
        workout = Workout.objects.filter(end_dt__isnull=True).first()
        if not workout:
            workout = Workout.objects.create(start_dt=timezone.now())
        kwargs["pk"] = workout.pk
        return super().get_redirect_url(*args, **kwargs)
    

class WorkoutView(generic.DetailView):
    template_name = "workouttracker/workout/workout.html"
    model = Workout


class WorkoutAddExerciseView(generic.CreateView):
    template_name = "workouttracker/workout/workout_exercise_form.html"
    model = WorkoutExercise
    form_class = WorkoutExerciseForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.workout_id = None
        self.enabled_metric_fields_by_exercise = get_enabled_metric_fields_by_exercise()
        self.default_metric_values_by_exercise = get_default_metric_values_by_exercise(self.enabled_metric_fields_by_exercise)

    def dispatch(self, request, *args, **kwargs):
        self.workout_id = kwargs["workout_id"]
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        initial["exercise"] = None
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout"] = Workout.objects.get(id=self.workout_id)
        context["all_metric_fields"] = Exercise.get_all_metric_fields()
        context["enabled_metric_fields_by_exercise"] = self.enabled_metric_fields_by_exercise
        context["default_metric_values_by_exercise"] = self.default_metric_values_by_exercise
        return context
    
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.workout_id = self.workout_id
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workout", kwargs={"pk": self.workout_id})
    

class WorkoutUpdateExerciseView(generic.UpdateView):
    template_name = "workouttracker/workout/workout_exercise_form.html"
    model = WorkoutExercise
    form_class = WorkoutExerciseForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workout"] = self.object.workout
        return context

    def get_success_url(self):
        return reverse_lazy("workout", kwargs={"pk": self.object.workout.id})


class WorkoutIncrementExerciseSetsView(generic.View):
    def post(self, request, *args, **kwargs):
        workout_exercise = WorkoutExercise.objects.get(id=kwargs["pk"])
        workout_exercise.sets += 1
        workout_exercise.save()
        return HttpResponse(workout_exercise.sets)
    

class WorkoutEndView(generic.UpdateView):
    template_name = "workouttracker/workout/workout_exercise_form.html"
    model = Workout
    form_class = WorkoutEndForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.end_dt = timezone.now()
        obj.save()
        return super().form_valid(form)
    

class WorkoutPreviousListView(generic.ListView):
    template_name = "workouttracker/workout/workout_previous_list.html"
    model = Workout
    queryset = Workout.objects.filter(end_dt__isnull=False).order_by("-start_dt")
    

class ExerciseListView(generic.ListView):
    template_name = "workouttracker/edit/exercise_list.html"
    model = Exercise


class ExerciseCreateView(generic.CreateView):
    template_name = "workouttracker/edit/exercise_form.html"
    model = Exercise
    form_class = ExerciseForm
    success_url = reverse_lazy("exercise_list")


class ExerciseUpdateView(generic.UpdateView):
    template_name = "workouttracker/edit/exercise_form.html"
    model = Exercise
    form_class = ExerciseForm
    success_url = reverse_lazy("exercise_list")


class ExerciseDeleteView(generic.DeleteView):
    template_name = "workouttracker/edit/exercise_delete.html"
    model = Exercise
    success_url = reverse_lazy("exercise_list")


class StatisticsView(generic.TemplateView):
    template_name = "workouttracker/statistics/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exercises"] = Exercise.objects.all()
        context["weight_data_points"] = [(w.start_dt.strftime("%m-%d-%Y %H:%M"), w.weight) for w in Workout.objects.filter(weight__isnull=False)]
        return context


class StatisticsExerciseDataPointsView(generic.View):
    def get(self, request, *args, **kwargs):
        exercise = Exercise.objects.get(id=kwargs["pk"])
        workout_exercises = WorkoutExercise.objects.filter(exercise=exercise)
        data_points = {capitalise_and_underscore_to_space(metric_field_name): [(workout_exercise.workout.start_dt.strftime("%m-%d-%Y %H:%M"), metric_value.seconds if metric_field_name == "duration" else metric_value) for workout_exercise in workout_exercises if (metric_value := getattr(workout_exercise, metric_field_name)) is not None] for metric_field_name in exercise.get_enabled_metric_fields()}
        return JsonResponse(data_points)
