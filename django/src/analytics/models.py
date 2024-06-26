from django.db import models

from app.models import EventLogModel
from app.models import TimestampedModel


class AUser(TimestampedModel):
    """
    replicates the User model from the Users app
    """

    class Meta:
        db_table = "analytics_user"

    public_id = models.UUIDField(unique=True)

    role = models.CharField(
        max_length=100,
        default="WORKER",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.public_id}"


class ATask(TimestampedModel):
    class Meta:
        db_table = "analytics_task"

    public_id = models.UUIDField(unique=True, blank=False, null=False)

    assignee_public_id = models.UUIDField(null=True)

    status = models.CharField(
        max_length=100,
    )

    cost_assign = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )

    cost_complete = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
    )

    # just in case (not needed for billing per se)
    title = models.CharField(
        max_length=100,
    )


class ATransaction(TimestampedModel):
    class Meta:
        db_table = "analytics_transaction"

    tx_id = models.CharField(unique=True, max_length=50)

    billing_cycle_id = models.DateField(blank=False, null=False)

    account = models.CharField(max_length=100, blank=False, null=False)

    description = models.CharField(max_length=100)

    type = models.CharField(
        max_length=100,
        blank=False,
        null=False,
    )

    credit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    debit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )


class ATaskLog(EventLogModel):
    class Meta:
        db_table = "analytics_task_log"


class ATransactionLog(EventLogModel):
    class Meta:
        db_table = "analytics_transaction_log"
