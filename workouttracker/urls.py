from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.IndexView.as_view(), login_url="/login/"), name='index'),
    path('workout_start', login_required(views.WorkoutStartView.as_view()), name="workout_start"),
    path('workout/<int:pk>/', login_required(views.WorkoutView.as_view()), name='workout'),
    path('workout/<int:workout_id>/add_exercise/', login_required(views.WorkoutAddExerciseView.as_view()), name='workout_add_exercise'),
    path('workout/update_exercise/<int:pk>/', login_required(views.WorkoutUpdateExerciseView.as_view()), name='workout_update_exercise'),
    path('workout/increment_exercise_sets/<int:pk>/', login_required(views.WorkoutIncrementExerciseSetsView.as_view()), name='workout_increment_exercise_sets'),
    path('workout/<int:pk>/end/', login_required(views.WorkoutEndView.as_view()), name='workout_end'),
    path('workout/previous_list/', login_required(views.WorkoutPreviousListView.as_view()), name='workout_previous_list'),
    path('exercise_list/', login_required(views.ExerciseListView.as_view()), name='exercise_list'),
    path('exercise_create/', login_required(views.ExerciseCreateView.as_view()), name='exercise_create'),
    path('exercise_update/<int:pk>/', login_required(views.ExerciseUpdateView.as_view()), name='exercise_update'),
    path('exercise_delete/<int:pk>/', login_required(views.ExerciseDeleteView.as_view()), name='exercise_delete'),
]
