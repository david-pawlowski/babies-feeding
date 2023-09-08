from django.utils import timezone

from django.contrib import admin
from babies.models import Baby, Food, Feeding
from babies.tasks import send_feeding_mail


TWO_HOURS_IN_S = 60 * 60 * 2


class FeedingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        t = timezone.now() - obj.created_at
        countdown = TWO_HOURS_IN_S - t.total_seconds()
        if t.total_seconds() > TWO_HOURS_IN_S:
            countdown = None            
        send_feeding_mail(
            mail_subject="Feeding time!",
            target_mail=obj.created_by.email,
            message=f"Last feeding with {obj.food} at {obj.created_at}",
        ).apply_async(countdown=countdown)
        super().save_model(request, obj, form, change)


admin.site.register(Baby)
admin.site.register(Food)
admin.site.register(Feeding, FeedingAdmin)
