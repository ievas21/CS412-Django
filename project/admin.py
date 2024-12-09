from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Book)
admin.site.register(Person)
admin.site.register(Review)
admin.site.register(Friend)
admin.site.register(BookList)
