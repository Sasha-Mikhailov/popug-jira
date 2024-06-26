# Generated by Django 4.2.7 on 2024-03-10 06:08

import uuid

from django.db import migrations
from django.db import models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TaskUser",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("public_id", models.UUIDField(unique=True)),
                ("role", models.CharField(max_length=100)),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("public_id", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("status", models.CharField(choices=[("ASSIGNED", "Assigned"), ("COMPLETED", "Completed")], default="ASSIGNED", max_length=100)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="tasks.taskuser")),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
