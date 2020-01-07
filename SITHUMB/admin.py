from django.contrib import admin
from .models import Activity, Examiner, Candidate, Section, Application, Photo
# Register your models here.
admin.site.register(Activity)
admin.site.register(Examiner)
admin.site.register(Candidate)
admin.site.register(Section)
admin.site.register(Application)
admin.site.register(Photo)