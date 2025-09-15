from django.contrib import admin
from .models import Person,Question,answer

# Register your models here.

admin.site.register(Person)
admin.site.register(Question)
admin.site.register(answer)
