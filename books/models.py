from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    number_of_pages = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class WorkOrder(models.Model):
    RATE_CHOICES = (
        ('Work Order', 'Work Order'),
        ('CS', 'CS'),
        ('Rate', 'Rate'),
    )
    rate_type = models.CharField(max_length=10, choices=RATE_CHOICES, default='Work Order')
    project = models.CharField(max_length=150)
    vendor = models.CharField(max_length=150)
    category = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.rate_type}-{self.category}-{self.vendor}-{self.project}"


class Bill(models.Model):
    project = models.CharField(max_length=150)
    category = models.CharField(max_length=150)
    vendor = models.CharField(max_length=150)
    wo = models.ManyToManyField(WorkOrder)
    ra = models.IntegerField(default=0)

    def ordinal_number(self):
        if 10 <= self.ra % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(self.ra % 10, "th")
        return str(self.ra) + suffix

    def total_amount(self):
        items = Item.objects.filter(bill=self)
        amount = sum(item.amount() for item in items)
        return round(amount, 2)

    def __str__(self):
        return f"{self.ordinal_number()} R/A--{self.project}--{self.vendor}"


class WorkOrderItem(models.Model):
    item_no = models.CharField(max_length=150)
    item_name = models.CharField(max_length=150)
    rate = models.FloatField(default=0)
    wo = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)

    def search_text(self):
        return f"{self.item_no} {self.item_name} {self.rate} {self.wo.__str__()}"

    def __str__(self):
        return self.item_name


class Item(models.Model):
    location = models.CharField(max_length=150)
    quantity = models.FloatField(default=0)
    quantity_parc = models.FloatField(default=1)
    rate_parc = models.FloatField(default=1)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    item = models.ForeignKey(WorkOrderItem, on_delete=models.CASCADE)

    def search_text(self):
        return f"{self.location} {self.quantity} {self.bill.__str__()}"

    def amount(self):
        if self.item_id is not None:
            work_order = self.item  # Access the related WorkOrder instance
            total = work_order.rate * self.quantity * 0.01 * self.quantity_parc * 0.01 * self.rate_parc
            return round(total, 2)
        return 0  # Handle the case where the item is not linked to a WorkOrder or the rate is not set
