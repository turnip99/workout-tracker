from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML, Field
from django import forms
from django.urls import reverse_lazy

from project.forms import FormWithHelperMixin
from workouttracker.utils import get_enabled_metric_fields_by_exercise
from .models import Exercise, WorkoutExercise


class ExerciseForm(FormWithHelperMixin, forms.ModelForm):
    class Meta:
        model = Exercise
        fields = [
            "name",
            "category",
            "weight_measured",
            "reps_measured",
            "duration_measured",
            "distance_measured",
            "difficulty_level_measured",
            "image",
            "notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.layout.append(Submit('submit', self.submit_text, css_class=self.submit_css_class))
        if self.instance.pk:
            self.helper.layout.append(HTML(f"<a class='btn btn-danger{' disabled' if self.instance.workoutexercise_set.exists() else ''}' href='{reverse_lazy('exercise_delete', kwargs={'pk': self.instance.pk})}'>Delete</a>"))


class WorkoutExerciseForm(FormWithHelperMixin, forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = [
            "exercise",
            "weight",
            "reps",
            "duration",
            "distance",
            "difficulty_level",
            "sets",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_metric_fields = Exercise.get_all_metric_fields()
        if self.instance.pk:
            self.fields.pop("exercise")
            enabled_metric_fields = self.instance.exercise.get_enabled_metric_fields()
            for field in all_metric_fields:
                if field not in enabled_metric_fields:
                    self.fields.pop(field)
        layout = Layout(
            "exercise",
            HTML(f"<div id='div_notes' class='fw-light fst-italic mb-3' style='white-space: pre-wrap'>{self.instance.exercise.notes if self.instance.pk and self.instance.exercise.notes else ""}</div>"),
            *[Field(metric_field) if metric_field in self.fields else None for metric_field in all_metric_fields],
            HTML("<hr/>"),
            "sets",
            Submit('submit', self.submit_text, css_class=self.submit_css_class)
        )
        self.helper = FormHelper(self)
        self.helper.layout = layout


class WorkoutEndForm(FormWithHelperMixin, forms.ModelForm):
    submit_text = "End workout"
    submit_css_class = "btn-success w-100"

    class Meta:
        model = WorkoutExercise
        fields = [
            "weight",
        ]
