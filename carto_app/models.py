from django.db import models
import uuid

class Serveur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    localisation = models.CharField(max_length=100)
    cycle_vie = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class ServiceMetier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    serveur = models.ForeignKey(Serveur, on_delete=models.CASCADE, related_name='applications')
    cycle_vie = models.CharField(max_length=50)
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class BaseDeDonnees(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    serveur = models.ForeignKey(Serveur, on_delete=models.CASCADE, related_name='bases')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='bases')
    cycle_vie = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Interface(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    protocole = models.CharField(max_length=50)
    source_application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interfaces_source')
    cible_application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interfaces_cible')

    def __str__(self):
        return f"{self.source_application} -> {self.cible_application} ({self.nom})"

class AppServiceMetier(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    service_metier = models.ForeignKey(ServiceMetier, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('application', 'service_metier')

class Utilisateur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    fonction = models.CharField(max_length=100)
    service_metier = models.ForeignKey(ServiceMetier, on_delete=models.CASCADE, related_name='utilisateurs')

    def __str__(self):
        return f"{self.prenom} {self.nom}"
