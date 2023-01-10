from django.contrib import admin
from .models import Todo

'''Display read-only fields'''


class TodoAdmin(admin.ModelAdmin):
	readonly_fields = ('created_at',)


admin.site.register(Todo, TodoAdmin)
