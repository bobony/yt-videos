from django.contrib import admin
from .models import ListItems

class ListItemsAdmin(admin.ModelAdmin):
	class Meta:
		model=ListItems
admin.site.register(ListItems,ListItemsAdmin)
