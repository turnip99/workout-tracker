from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.formats.base_formats import CSV

from .models import Exercise, Workout, WorkoutExercise

class CustomImportExportModelAdmin(ImportExportModelAdmin):
  formats = [CSV]



@admin.register(Exercise)
class ExerciseAdmin(CustomImportExportModelAdmin):
    pass


@admin.register(Workout)
class WorkoutAdmin(CustomImportExportModelAdmin):
    pass


@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(CustomImportExportModelAdmin):
    pass