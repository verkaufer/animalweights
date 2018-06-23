from django.contrib import admin

# Register your models here.
from animals.models import Animal, Weight

admin.site.register(Animal)
admin.site.register(Weight)
