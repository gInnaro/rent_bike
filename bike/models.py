from django.db import models

class Bicycle(models.Model):
    AVAILABLE = 'available'
    RENTED = 'rented'
    STATUS_CHOICES = [
        (AVAILABLE, 'Доступен'),
        (RENTED, 'Арендован'),
    ]
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    price = models.IntegerField(default=10)
    username = models.CharField(max_length=255, blank=True, null=True, default=None if status == AVAILABLE else '')
    rent_start = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = 'Велосипед'
        verbose_name_plural = 'Велосипеды'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.status == self.AVAILABLE:
            self.username = None
            self.rent_start = None
        super().save(*args, **kwargs)


class RentailHistory(models.Model):
    bicycle_id = models.IntegerField()
    bicycle_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    rental_cost = models.FloatField()
    rental_minute = models.FloatField()
    rent_start = models.DateTimeField(blank=True, null=True)
    rent_end = models.DateTimeField(blank=True, null=True)


    class Meta:
        verbose_name = 'Журнал аренды велосипедов'
        verbose_name_plural = 'Журнал аренды велосипедов'
