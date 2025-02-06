from django.urls import path
from .views import classify_number_view

urlpatterns = [
  path('classify-number/', classify_number_view, name='classify-numbers')
]
