# Generated by Django 3.2.6 on 2023-08-19 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=150)),
                ('category', models.CharField(max_length=150)),
                ('vendor', models.CharField(max_length=150)),
                ('ra', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_no', models.CharField(max_length=150)),
                ('item_name', models.CharField(max_length=150)),
                ('rate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=150)),
                ('quantity', models.FloatField(default=0)),
                ('quantity_parc', models.FloatField(default=1)),
                ('rate_parc', models.FloatField(default=1)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.bill')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.workorder')),
            ],
        ),
    ]