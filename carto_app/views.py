from django.shortcuts import render
from django.db import connection
from django.http import JsonResponse
from .models import Serveur, Application, BaseDeDonnees, ServiceMetier, AppServiceMetier, Interface

def impact_serveur(request):
    serveurs = Serveur.objects.all()
    serveur_id = request.GET.get("serveur_id")
    selected = None
    applications = []
    bdds = []

    if serveur_id:
        try:
            selected = Serveur.objects.get(id=serveur_id)
            applications = Application.objects.filter(serveur=selected)
            bdds = BaseDeDonnees.objects.filter(serveur=selected)
        except Serveur.DoesNotExist:
            selected = None

    return render(request, "impact.html", {
        "serveurs": serveurs,
        "selected": selected,
        "applications": applications,
        "bdds": bdds,
    })

def requete_sql(request):
    result = []
    headers = []
    sql = ""
    error = None
    serveurs = Serveur.objects.all()

    if request.method == "POST":
        sql = request.POST.get("sql", "")
        if sql.strip().lower().startswith("select"):
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    headers = [col[0] for col in cursor.description]
                    result = cursor.fetchall()
            except Exception as e:
                error = str(e)
        else:
            error = "Seules les requêtes SELECT sont autorisées."

    return render(request, "requete_sql.html", {
        "sql": sql,
        "headers": headers,
        "result": result,
        "error": error,
        "serveurs": serveurs,
    })

def visualisation(request):
    return render(request, "visualisation.html")

def visualisation_data(request):
    serveur_filtre = request.GET.get("serveur")
    data = []
    serveurs = Serveur.objects.all()

    if serveur_filtre:
        serveurs = serveurs.filter(nom=serveur_filtre)

    for serveur in serveurs:
        apps = []
        for app in Application.objects.filter(serveur=serveur):
            services = ServiceMetier.objects.filter(
                id__in=AppServiceMetier.objects.filter(application=app).values_list('service_metier_id', flat=True)
            )
            apps.append({
                "nom": app.nom,
                "version": app.version,
                "services": [s.nom for s in services]
            })
        data.append({
            "serveur": serveur.nom,
            "applications": apps
        })

    return JsonResponse(data, safe=False)

def diagramme_applications(request):
    data = []
    serveurs = Serveur.objects.all()
    liens = AppServiceMetier.objects.select_related("application", "service_metier")

    for lien in liens:
        data.append({
            "application": lien.application.nom,
            "service_metier": lien.service_metier.nom,
            "serveur": lien.application.serveur.nom if lien.application.serveur else "Aucun serveur"
        })

    return render(request, "diagramme.html", {
        "data": data,
        "serveurs": serveurs,
    })

def visualisation_arborescente(request):
    services = ServiceMetier.objects.prefetch_related(
        'appservicemetier_set__application__bases',
        'appservicemetier_set__application__serveur'
    )
    return render(request, 'visualisation_arborescente.html', {'services': services})

def data_hierarchique(request):
    data = []

    for service in ServiceMetier.objects.all():
        service_data = {
            "name": service.nom,
            "children": []
        }
        apps = Application.objects.filter(appservicemetier__service_metier=service)
        for app in apps:
            app_data = {
                "name": app.nom,
                "children": []
            }
            bdds = BaseDeDonnees.objects.filter(application=app)
            for bdd in bdds:
                app_data["children"].append({
                    "name": bdd.nom,
                    "type": "Base de données",
                    "serveur": bdd.serveur.nom if bdd.serveur else "Non attribué"
                })
            service_data["children"].append(app_data)
        data.append(service_data)

    return JsonResponse({"name": "Système d'information", "children": data})

def vue_arbre(request):
    return render(request, "arbre.html")

def api_hierarchie(request):
    def build_tree():
        result = []
        for service in ServiceMetier.objects.all():
            service_node = {
                "name": service.nom,
                "children": []
            }
            for asm in service.appservicemetier_set.select_related('application'):
                app = asm.application
                app_node = {
                    "name": app.nom,
                    "children": []
                }
                if app.serveur:
                    app_node["children"].append({"name": f"Serveur: {app.serveur.nom}"})
                service_node["children"].append(app_node)
            result.append(service_node)
        return {"name": "Système d'information", "children": result}

    return JsonResponse(build_tree())

def liste_serveurs(request):
    serveurs = Serveur.objects.all()
    return render(request, "serveurs.html", {"serveurs": serveurs})

def get_visualisation_data(request):
    def build_application_node(app):
        # Récupérer services métiers
        services = ServiceMetier.objects.filter(appservicemetier__application=app)
        services_nodes = [
            {"name": f"Service : {s.nom}", "type": "service_metier"} for s in services
        ]

        # Récupérer bases de données
        bdd_nodes = [
            {"name": f"BDD : {bdd.nom}", "type": "bdd"}
            for bdd in app.bases.all()
        ]

        # Récupérer interfaces (vers autres apps)
        interfaces = Interface.objects.filter(source_application=app)
        interfaces_nodes = [
            {"name": f"Interface → {i.cible_application.nom}", "type": "interface"}
            for i in interfaces
        ]

        children = bdd_nodes + services_nodes + interfaces_nodes

        return {
            "name": f"App : {app.nom}",
            "type": "application",
            "children": children
        }

    data = []
    for serveur in Serveur.objects.prefetch_related('applications__bases'):
        apps_nodes = [build_application_node(app) for app in serveur.applications.all()]
        serveur_node = {
            "name": f"Serveur : {serveur.nom}",
            "type": "serveur",
            "children": apps_nodes
        }
        data.append(serveur_node)

    return JsonResponse({"name": "Système d'information", "type": "root", "children": data})