from django.http.response import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BillForm, WorkOrderForm, WorkOrderItemForm, ItemForm
from .models import Bill, WorkOrder, WorkOrderItem, Item
from django.db.models import Q


def bill_list(request):
    bill = Bill.objects.all()
    context = {
        'bills': bill
    }
    return render(request, 'partials/bill_list.html', context)


def wo_list(request):
    wo = WorkOrder.objects.all()
    context = {
        'work_order': wo
    }
    return render(request, 'partials/wo_list.html', context)


def create_bill(request):
    form = BillForm(request.POST or None)
    wo = WorkOrder.objects.all()
    if request.method == "POST":
        if form.is_valid():
            bill = form.save(commit=False)
            bill.save()
            form.save_m2m()
            return redirect('create-bill-item', pk=bill.id)
    context = {
        'form': form,
        'work_orders': wo
    }
    return render(request, "bill_form.html", context)


def create_bill_item(request, pk):
    bill = Bill.objects.get(id=pk)
    form = ItemForm(request.POST or None)
    item = Item.objects.filter(bill=bill)
    total_amount = 0
    for i in item:
        total_amount += i.amount()
    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.bill = bill
            item.save()
            return redirect("detail-bill-item", pk=item.id)
        else:
            return render(request, "partials/bill_item_form.html", context={
                "form": form
            })
    context = {
        'form': form,
        'bill': bill,
        'bill_items': item,
        'total_amount': round(total_amount, 2)
    }
    return render(request, "bill_form_htmx.html", context)


def create_work_order(request):
    form = WorkOrderForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            wo = form.save(commit=False)
            wo.save()
            context = {
                'wo': wo
            }
            return redirect('create-wo-item', pk=wo.id)
    context = {
        'form': form
    }
    return render(request, "wo_form.html", context)


def create_work_order_item(request, pk):
    wo = WorkOrder.objects.get(id=pk)
    form = WorkOrderItemForm(request.POST or None)
    wo_item = WorkOrderItem.objects.filter(wo=wo)

    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.wo = wo
            item.save()
            return redirect("detail-item", pk=item.id)
        else:
            return render(request, "partials/wo_item_form.html", context={
                "form": form
            })
    context = {
        'form': form,
        'wo': wo,
        'wo_items': wo_item
    }
    return render(request, "wo_form_htmx.html", context)


def wo_item_form(request):
    form = WorkOrderItemForm()
    context = {
        'form':form
    }
    return render(request, "partials/wo_item_form.html", context)


def bill_item_form(request, pk):
    bill = Bill.objects.get(id=pk)
    form = ItemForm()
    work_orders = bill.wo.all()  # Get related WorkOrder instances

    # Collect related WorkOrderItem instances for each WorkOrder
    work_order_items = []
    for work_order in work_orders:
        work_order_items.extend(work_order.workorderitem_set.all())
    context = {
        'form': form,
        'wo_items': work_order_items,
        'bill': bill
    }
    return render(request, "partials/bill_item_form.html", context)


# def create_book(request, pk):
#     author = Author.objects.get(id=pk)
#     books = Book.objects.filter(author=author)
#     form = BookForm(request.POST or None)
#
#     if request.method == "POST":
#         if form.is_valid():
#             book = form.save(commit=False)
#             book.author = author
#             book.save()
#             return redirect("detail-book", pk=book.id)
#         else:
#             return render(request, "partials/book_form.html", context={
#                 "form": form
#             })
#
#     context = {
#         "form": form,
#         "author": author,
#         "books": books
#     }
#
#     return render(request, "create_book.html", context)


# def update_book(request, pk):
#     book = Book.objects.get(id=pk)
#     form = BookForm(request.POST or None, instance=book)
#
#     if request.method == "POST":
#         if form.is_valid():
#             form.save()
#             return redirect("detail-book", pk=book.id)
#
#     context = {
#         "form": form,
#         "book": book
#     }
#
#     return render(request, "partials/book_form.html", context)


def update_wo_item(request, pk):
    wo_item = WorkOrderItem.objects.get(id=pk)
    form = WorkOrderItemForm(request.POST or None, instance=wo_item)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("detail-item", pk=wo_item.id)

    context = {
        "form": form,
        "wo_item": wo_item
    }

    return render(request, "partials/wo_item_form.html", context)


def update_bill_item(request, pk):
    bill_item = Item.objects.get(id=pk)
    bill = bill_item.bill
    form = ItemForm(request.POST or None, instance=bill_item)
    work_orders = bill.wo.all()  # Get related WorkOrder instances

    # Collect related WorkOrderItem instances for each WorkOrder
    work_order_items = []
    for work_order in work_orders:
        work_order_items.extend(work_order.workorderitem_set.all())

    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            item.save()

            return redirect("detail-bill-item", pk=bill_item.id)

    context = {
        'form': form,
        'wo_items': work_order_items,
        'bill': bill,
        'bill_item': bill_item
    }

    return render(request, "partials/bill_item_form.html", context)


def delete_wo_item(request, pk):
    wo_item = get_object_or_404(WorkOrderItem, id=pk)

    if request.method == "POST":
        wo_item.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )


def delete_bill_item(request, pk):
    bill_item = get_object_or_404(Item, id=pk)

    if request.method == "POST":
        bill_item.delete()
        return HttpResponse("")

    return HttpResponseNotAllowed(
        [
            "POST",
        ]
    )



def detail_wo_item(request, pk):
    wo_item = get_object_or_404(WorkOrderItem, id=pk)
    context = {
        "wo_item": wo_item
    }
    return render(request, "partials/wo_item_detail.html", context)


def detail_bill_item(request, pk):
    bill_item = get_object_or_404(Item, id=pk)
    context = {
        "bill_item": bill_item
    }
    return render(request, "partials/bill_item_detail.html", context)


def search(request):
    query = request.GET.get('query')
    s_type = request.GET.get('type')
    project = request.GET.get('project')
    unique_projects = Bill.objects.values_list('project', flat=True).distinct()
    project_array = list(unique_projects)
    total_quantity = 0
    search_item =[]
    if query and s_type and project:
        if s_type == "Work Order":
            wo_item = WorkOrderItem.objects.filter(
            Q(item_no__icontains=query) |
            Q(item_name__icontains=query) |
            Q(rate__icontains=query) |
            Q(wo__vendor__icontains=query)
            )
            search_item = Item.objects.filter(item__in=wo_item, bill__project=project)
            for s in search_item:
                total_quantity += (s.quantity * s.quantity_parc * 0.01)
        elif s_type == "Bill Location":
            search_item = Item.objects.filter(
            Q(location__icontains=query) |
            Q(quantity__icontains=query),
            bill__project=project
            )
            for s in search_item:
                total_quantity += (s.quantity * s.quantity_parc * 0.01)
    context = {
        'search_item': search_item,
        'projects': project_array,
        'total_quantity': total_quantity
    }
    return render(request, 'partials/search.html', context)


# def create_book_form(request):
#     form = BookForm()
#     context = {
#         "form": form
#     }
#     return render(request, "partials/book_form.html", context)
