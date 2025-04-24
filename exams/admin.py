from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'category', 'correct')
    search_fields = ('text',)
# Register your models here.
