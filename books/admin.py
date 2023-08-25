from django.contrib import admin
from .models import WorkOrder, WorkOrderItem, Bill


class ItemInlineAdmin(admin.TabularInline):
    model = WorkOrderItem

admin.site.register(Bill)


class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [ItemInlineAdmin]


admin.site.register(WorkOrder, WorkOrderAdmin)
