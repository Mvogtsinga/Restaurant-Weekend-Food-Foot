from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class TableType(models.Model):
    TYPE_CHOICES = [
        ('COUPLE', 'Couple'),
        ('FAMILIAL', 'Familial'),
        ('INDIVIDUAL', 'Individuel'),
        ('VIP', 'VIP'),
        ('EXTRA_FAMILLE', 'Extra Famille'),
        ('FAMILIAL_MIXTE', 'Famille Mixte'),
    ]
    name = models.CharField(max_length=50, choices=TYPE_CHOICES, unique=True)
    seats = models.IntegerField(default=2)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_path = models.CharField(max_length=100, default='path/to/default/image.jpg')

    def __str__(self):
        return f"{self.get_name_display()} ({self.seats} places)"
    
    def is_available(self, reservation_date, reservation_time, reservation_duration):
        now = datetime.combine(reservation_date, reservation_time)
        end_time = now + timedelta(hours=reservation_duration)
        reservations = Reservation.objects.filter(table_type=self, date=reservation_date, time__lt=end_time.time())
        return not reservations.exists()

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('V', 'Valide'),
        ('T', 'Terminé'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    duration = models.DurationField(default=timedelta(hours=2))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='V')

    class Meta:
        unique_together = ('table_type', 'date', 'time')

    def __str__(self):
        return f"{self.user.username} - {self.table_type} - {self.date} {self.time}"

    def save(self, *args, **kwargs):
        self.validate_availability()
        super().save(*args, **kwargs)

    def validate_availability(self):
        reservation_start = datetime.combine(self.date, self.time)
        reservation_end = reservation_start + self.duration
        overlapping_reservations = Reservation.objects.filter(
            table_type=self.table_type,
            date=self.date,
            time__lt=reservation_end.time()
        ).exclude(id=self.id)
        for reservation in overlapping_reservations:
            other_start = datetime.combine(reservation.date, reservation.time)
            other_end = other_start + reservation.duration
            if other_start < reservation_end and reservation_start < other_end:
                raise ValidationError(f"La table {self.table_type} n'est pas disponible à cette heure.")

    def status_color(self):
        now = timezone.now()
        reservation_end = timezone.make_aware(datetime.combine(self.date, self.time)) + self.duration
        if now < reservation_end:
            return 'text-danger'
        else:
            return 'text-success'

    def get_status_display(self):
        for status, display in self.STATUS_CHOICES:
            if status == self.status:
                return display
        return ''

    def end_time(self):
        reservation_start = datetime.combine(self.date, self.time)
        reservation_end = reservation_start + self.duration
        return reservation_end.time()
