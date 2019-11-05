from django.contrib import admin
from .models import Activity, Examiner, Candidate, Transcript, Application, Section
# Register your models here.
admin.site.register(Activity)
admin.site.register(Examiner)
admin.site.register(Candidate)
admin.site.register(Transcript)
admin.site.register(Application)
admin.site.register(Section)