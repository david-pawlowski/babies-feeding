import datetime
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

from babies.tasks import send_feeding_mail, send_push_notification


class User(AbstractUser):
    push_over_token = models.CharField(max_length=100, null=True)


class Baby(models.Model):
    name = models.CharField(max_length=100)
    age = models.DateField(null=True)
    feeding_interval = models.IntegerField(default=60)

    def __str__(self):
        return f"{self.name} {self.age_in_days} days"

    @property
    def age_in_days(self):
        return (datetime.date.today() - self.age).days


class Food(models.Model):
    name = models.CharField(max_length=100)
    natural = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Feeding(models.Model):
    created_at = models.DateTimeField()
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.IntegerField()
    baby = models.ForeignKey(Baby, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.baby}, {self.food} \
            at {self.created_at.strftime('%D %H:%M')}"

    def send_notification(self):
        feeding_interval = self.baby.feeding_interval
        t = timezone.now() - self.created_at
        countdown = feeding_interval - t.total_seconds()
        if t.total_seconds() > feeding_interval:
            countdown = 1
        send_feeding_mail.apply_async(
            args=(
                "Feeding time!",
                self.created_by.email,
                f"Last feeding with {self.food} \
                at {self.created_at.strftime('%H:%M')}",
            ),
            countdown=countdown,
        )
        send_push_notification.apply_async(
            args=(
                f"{self.baby.name} it is time to eat something! \
                    You ate {self.amount} {self.food} \
                        at {self.created_at.strftime('%H:%M')}.",
                self.created_by.push_over_token,
            ),
            countdown=countdown,
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.send_notification()
