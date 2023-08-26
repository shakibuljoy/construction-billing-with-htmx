from django.contrib import admin
from django.urls import path

from books.views import (
    create_bill,
    create_work_order,
    detail_wo_item,
    create_work_order_item,
    update_wo_item,
    delete_wo_item,
    wo_item_form,
    detail_bill_item,
    create_bill_item,
    delete_bill_item,
    update_bill_item,
    bill_item_form,
    bill_list,
    wo_list,
    search
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', search, name="search"),
    # Billing Part
    path('bill/', bill_list, name='bill-list'),
    path('create-bill/', create_bill, name='create-bill'),
    path('bill_item_form/<pk>/', bill_item_form, name='bill-item-form'),
    path('create-bill-item/<pk>/', create_bill_item, name='create-bill-item'),
    path('detail-bill-item/<pk>/', detail_bill_item, name='detail-bill-item'),
    path('delete-bill-item/<pk>/', delete_bill_item, name='delete-bill-item'),
    path('update-bill-item/<pk>/', update_bill_item, name='update-bill-item'),
    # Work Order Part
    path('work-order/', wo_list, name='wo-list'),
    path('create-work-order/', create_work_order, name='create-work-order'),
    path('wo-item-form/', wo_item_form, name='wo-item-form'),
    path('create-wo-item/<pk>/', create_work_order_item, name='create-wo-item'),
    path('update_wo_item/<pk>/', update_wo_item, name='update_wo_item'),
    path('detail_item/<pk>', detail_wo_item, name='detail-item'),
    path('delete_wo_item/<pk>', delete_wo_item, name='delete_wo_item'),
]
