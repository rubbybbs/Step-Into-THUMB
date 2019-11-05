from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    section_cnt = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    application_format = models.TextField()


class Section(models.Model):
    s_id = models.IntegerField()
    name = models.CharField(max_length=100, default="")
    from_date = models.DateField(default=None)
    to_date = models.DateField(default=None)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='sections')
    transcript_format = models.TextField(default="")


class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='examiners')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='examiners')


@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    if created:
        Examiner.objects.create(user=instance)
    else:
        instance.extension.save()


class Candidate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='candidates')
    examiners = models.ManyToManyField(Examiner)
    stage = models.IntegerField()


class Application(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='application')
    form = models.TextField(default="")


class Transcript(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='transcripts')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='transcript')
    form = models.TextField(default="")
