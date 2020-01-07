from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from filer.fields.image import FilerImageField


class Activity(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    status = models.IntegerField(default=0) # 0:活动制定中 1：活动发布
    section_cnt = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="")
    from_date = models.DateField(default=None)
    to_date = models.DateField(default=None)
    application_format = models.TextField(default="")
    admission_letter = models.TextField(default="")
    refusal_letter = models.TextField(default="")


class Candidate(models.Model):
    name = models.CharField(max_length=100, default="")
    student_id = models.CharField(max_length=100, default="")
    wx_id = models.CharField(max_length=100, default="")


class Application(models.Model):
    admitted = models.BooleanField(default=False)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications', null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='applications', null=True)
    stage = models.IntegerField(default=1)
    application_form = models.TextField(default="")
    transcript = models.TextField(default="")


class Photo(models.Model):
    image = FilerImageField(null=True, on_delete=models.CASCADE)


class Section(models.Model):
    s_id = models.IntegerField(default=0)
    compulsory = models.BooleanField(default=True)
    name = models.CharField(max_length=100, default="")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='sections', null=True)
    transcript_format = models.TextField(default="")
    checking = models.ManyToManyField(Application, related_name="checking_sections", blank=True)
    unqualified = models.ManyToManyField(Application, related_name="unqualified_sections", blank=True)
    qualified = models.ManyToManyField(Application, related_name="qualified_sections", blank=True)


class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension', null=True)
    username = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=256, default="")
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='examiners', null=True)
    sections = models.ManyToManyField(Section, blank=True)
    examinees = models.TextField(default="")


@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    if created:
        Examiner.objects.create(username=instance.username, user=instance)
    else:
        instance.extension.save()

