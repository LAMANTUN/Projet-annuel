from django.urls import path
from .views import impact_serveur, requete_sql, visualisation, visualisation_data , diagramme_applications, vue_arbre, api_hierarchie
from . import views

urlpatterns = [
    path('', impact_serveur, name='impact_serveur'),
    path('sql/', requete_sql, name='requete_sql'),
    path('visualisation/', visualisation, name='visualisation'),
    path('api/visualisation/', visualisation_data, name='visualisation_data'),
    path("diagramme/", diagramme_applications, name="diagramme_applications"),
    path('visualisation/', views.visualisation_arborescente, name='visualisation_arborescente'),
    path('arbre/', views.vue_arbre, name='vue_arbre'),
    path("data/arbre/", views.data_hierarchique, name="data_arbre"),
    path('api/hierarchie/', api_hierarchie, name='api_hierarchie'),

]


