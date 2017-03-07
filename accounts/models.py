from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class HousesFilter(models.Model):
    """House filter model."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filter_data_json = models.TextField('Filter Data', blank=True, null=True)
    active = models.BooleanField('Is active', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    """Profile model for extending User model fields."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show_photos_filters = models.BooleanField('Show title photo', default=False)
    font_ratio = models.FloatField('Font size', default=1)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = Profile.objects.get(user=self.user)
                self.pk = p.pk
            except Profile.DoesNotExist:
                pass

        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
