from django.urls import path
from .views import (
    impact_serveur,
    requete_sql,
    visualisation,
    visualisation_data,
    diagramme_applications,
    vue_arbre,
    api_hierarchie,
    visualisation_arborescente,
    data_hierarchique,
    liste_serveurs,  # ✅ ajout de ta nouvelle vue
)

urlpatterns = [
    path('', impact_serveur, name='impact_serveur'),
    path('sql/', requete_sql, name='requete_sql'),
    path('visualisation/', visualisation, name='visualisation'),
    path('api/visualisation/', visualisation_data, name='visualisation_data'),
    path('diagramme/', diagramme_applications, name='diagramme_applications'),
    path('visualisation_arborescente/', visualisation_arborescente, name='visualisation_arborescente'),
    path('arbre/', vue_arbre, name='vue_arbre'),
    path('data/arbre/', data_hierarchique, name='data_arbre'),
    path('api/hierarchie/', api_hierarchie, name='api_hierarchie'),

    # ✅ Nouvelle route pour l'affichage mosaïque des serveurs
    path('serveurs/', liste_serveurs, name='liste_serveurs'),
]
