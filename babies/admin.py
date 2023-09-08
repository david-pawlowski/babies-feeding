from django.utils import timezone

from django.contrib import admin
from babies.models import Baby, Food, Feeding, User
from babies.tasks import send_feeding_mail, send_push_notification


# TODO: Change it to be adjustable in the admin panel.
TWO_HOURS_IN_S = 60 * 60 * 2


class FeedingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        t = timezone.now() - obj.created_at
        countdown = TWO_HOURS_IN_S - t.total_seconds()
        if t.total_seconds() > TWO_HOURS_IN_S:
            countdown = 1
        send_feeding_mail.apply_async(
            args=(
                "Feeding time!",
                obj.created_by.email,
                f"Last feeding with {obj.food} at {obj.created_at.strftime('%H:%M')}",
            ),
            countdown=countdown,
        )
        send_push_notification.apply_async(
            args=(
                f"{obj.baby.name} it is time to eat something! \
                    You ate {obj.amount} {obj.food} at {obj.created_at.strftime('%H:%M')}.",
                obj.created_by.push_over_token,
            ),
            countdown=countdown,
        )
        super().save_model(request, obj, form, change)


admin.site.register(Baby)
admin.site.register(Food)
admin.site.register(Feeding, FeedingAdmin)
admin.site.register(User)
