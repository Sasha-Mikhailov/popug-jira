# Generated by Django 4.2.7 on 2024-03-16 12:12

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ATask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("public_id", models.UUIDField(unique=True)),
                ("assignee_public_id", models.UUIDField(null=True)),
                ("status", models.CharField(max_length=100)),
                ("cost_assign", models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ("cost_complete", models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ("title", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "analytics_task",
            },
        ),
        migrations.CreateModel(
            name="ATaskLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("event_id", models.UUIDField()),
                ("event_version", models.TextField(null=True)),
                ("event_name", models.TextField(null=True)),
                ("producer", models.TextField(null=True)),
                ("payload", models.JSONField()),
            ],
            options={
                "db_table": "analytics_task_log",
            },
        ),
        migrations.CreateModel(
            name="ATransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("tx_id", models.CharField(max_length=50, unique=True)),
                ("billing_cycle_id", models.DateField()),
                ("account", models.CharField(max_length=100)),
                ("description", models.CharField(max_length=100)),
                ("type", models.CharField(max_length=100)),
                ("credit", models.DecimalField(decimal_places=2, max_digits=10)),
                ("debit", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                "db_table": "analytics_transaction",
            },
        ),
        migrations.CreateModel(
            name="ATransactionLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("event_id", models.UUIDField()),
                ("event_version", models.TextField(null=True)),
                ("event_name", models.TextField(null=True)),
                ("producer", models.TextField(null=True)),
                ("payload", models.JSONField()),
            ],
            options={
                "db_table": "analytics_transaction_log",
            },
        ),
        migrations.CreateModel(
            name="AUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("public_id", models.UUIDField(unique=True)),
                ("role", models.CharField(default="WORKER", max_length=100)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "analytics_user",
            },
        ),
    ]
