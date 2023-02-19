from django.contrib import admin
from .models import Expense, Category

# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('owner', 'category', 'amount', 'description')
    search_fields = ('category', 'description')

admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)