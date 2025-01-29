from django.db import models
from django.utils import timezone


# Model for class schedules
class Schedule(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]

    name = models.CharField(max_length=100)  # Nom du cours
    day = models.CharField(max_length=9, choices=DAY_CHOICES)  # Jour du cours
    start_time = models.TimeField()  # Heure de début
    end_time = models.TimeField()  # Heure de fin
    instructor = models.CharField(max_length=100)  # Nom de l'instructeur
    max_participants = models.PositiveIntegerField(default=10)  # Nombre maximum de participants
   

    def __str__(self):
        return f"{self.name} - {self.day} {self.start_time} - {self.end_time}"

# Model for client registration
class ClientRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    contact = models.CharField(max_length=20)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='registrations')
    payment_on_day = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)  # Nouveau champ pour stocker l'ID de paiement Stripe

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.schedule.name} on {self.schedule.day}"

