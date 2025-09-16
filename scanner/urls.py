from django.urls import path
from . import views

urlpatterns = [
    # This rule says: for the homepage (''), run the 'index' function from views.py
    path('', views.index, name='index'),
    
    # This rule says: for the '/analyze/' URL, run the 'analyze' function from views.py
    path('analyze/', views.analyze, name='analyze'),
]
