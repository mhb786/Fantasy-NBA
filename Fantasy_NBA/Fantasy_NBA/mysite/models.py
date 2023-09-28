from django.db import models

# Create your models here.

class NBAPlayer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    team = models.CharField(max_length=50, default='Unknown')

    PPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    APG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    RPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    SPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    BPG = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    FG_PCT = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    FG3_PCT = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    FT_PCT = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    MIN = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    TOV = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

