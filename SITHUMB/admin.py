from django.contrib import admin
from .models import Activity, Examiner, Candidate, Section, Application
# Register your models here.
admin.site.register(Activity)
admin.site.register(Examiner)
admin.site.register(Candidate)
admin.site.register(Section)
admin.site.register(Application)
