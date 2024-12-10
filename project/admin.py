from django.contrib import admin
from .models import *

# Register your models here.

# register our models to be on the admin page for manual manipulation
admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Review)
admin.site.register(Friend)
admin.site.register(BookList)
