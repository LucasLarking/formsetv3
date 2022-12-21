from django.contrib import admin

# Register your models here.
from .models import (
    Survey,
    Question,
    Option,
    Answer,

)

# Register your models here.
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)


