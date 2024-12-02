from django.db import models
from django.contrib.auth.models import User

# Models for reservation app.

class Route(models.Model):
    start_city = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.start_city} to {self.destination}"

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    seat_number = models.IntegerField()
    STATUS_CHOICES = [
    ('active', 'Active'),
    ('cancelled', 'Cancelled'),]
    status = models.CharField(max_length=50, default='active')  # active or cancelled

    def __str__(self):
        return f"Ticket for {self.user.username} - {self.route.start_city} to {self.route.destination}"
    
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.created_at}"

