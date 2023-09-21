from django.db import models

# Create your models here.

class NBAPlayer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.CharField(max_length=50, default='Unknown')
    # Add more fields as needed (e.g., height, weight, position, etc.)

    points_per_game = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assists_per_game = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rebounds_per_game = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
