from django import forms

from .models import Bill, Item, WorkOrder, WorkOrderItem


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = (
            'project',
            'category',
            'vendor',
            'ra',
            'wo'
        )


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
            'location',
            'quantity',
            'quantity_parc',
            'rate_parc',
            'item'
        )


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = (
            'project',
            'category',
            'vendor',
            'rate_type',
        )


class WorkOrderItemForm(forms.ModelForm):
    class Meta:
        model = WorkOrderItem
        fields = (
            'item_no',
            'item_name',
            'rate',
            'unit'
        )

