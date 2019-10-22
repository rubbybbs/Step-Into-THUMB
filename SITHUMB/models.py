from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Activity(models.Model):
    name = models.CharField(max_length=100)
    application_format = models.TextField()
    transcript_format = models.TextField()


class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activity = models.ManyToManyField(Activity)


@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    if created:
        Examiner.objects.create(user=instance)
    else:
        instance.extension.save()


class Candidate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    examiners = models.ManyToManyField(Examiner)
    stage = models.IntegerField()


class Application(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    form = models.TextField()


class Transcript(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    form = models.TextField()

