from django.urls import path

from animals.views import (AnimalListView, AnimalDetailView, RecordWeightView,
                           EstimatedWeightView)

app_name = 'animals'

urlpatterns = [
    path('', AnimalListView.as_view(), name='all_animals'),
    path('<int:pk>/', AnimalDetailView.as_view(), name='animal_detail'),
    path('<int:pk>/weight/', RecordWeightView.as_view(), name='record_weight'),
    path('<int:pk>/estimated-weight/', EstimatedWeightView.as_view(), name='estimated_weight')
]
