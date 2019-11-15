import django
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Activity(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    section_cnt = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    from_date = models.DateField(default=None)
    to_date = models.DateField(default=None)
    application_format = models.TextField()


class Section(models.Model):
    a_id = models.IntegerField(default=0)
    s_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='sections', null=True)
    transcript_format = models.TextField(default="")


class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension', null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='examiners', null=True)
    sections = models.ManyToManyField(Section)


@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    if created:
        Examiner.objects.create(user=instance)
    else:
        instance.extension.save()


class Candidate(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='candidates', null=True)
    examiners = models.ManyToManyField(Examiner)
    stage = models.IntegerField(default=0)


class Application(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='applications', null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='application', null=True)
    form = models.TextField(default="")


class Transcript(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='transcripts', null=True)
    section = models.ForeignKey(Section,  on_delete=models.CASCADE, related_name='transcripts', null=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='transcripts', null=True)
    form = models.TextField(default="")
