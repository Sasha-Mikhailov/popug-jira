from django.db.utils import IntegrityError

from app.settings import DEBUG
from app.settings import Topics
from billing.models import BillingTask
from billing.models import BillingUser
from kafka_app.consumer import Consumer
from kafka_app.producer import Producer

p = Producer()


class BillingTaskConsumer(Consumer):
    def do_work(self, record_key, record_data):
        payload = record_data.get("payload", {})
        print(f"consumed message with key {record_key}; " f"meta {record_data}; " f"payload {payload}")

        try:
            if (record_data["event_name"] == "tasks.task-created") & (str(record_data["event_version"]) == "1"):
                task = BillingTask(
                    public_id=payload["public_id"],
                    created=payload["created"],
                    assignee_public_id=payload["assignee_public_id"],
                    title=payload["title"],
                    status=payload["status"],
                )
                task.save()
                print(f"created task {task} with status {task}")

            elif (record_data["event_name"] == "tasks.task-completed") & (str(record_data["event_version"]) == "1"):
                if BillingTask.objects.filter(public_id=payload["public_id"]).exists():
                    task = BillingTask.objects.get(public_id=payload["public_id"])
                    task.status = payload["new_status"]
                    task.save()
                    print(f"updated task {task} with status {payload['new_status']}")
                else:
                    # FIXME handle via DLQ — no task in DB to complete yet
                    print(f"ERROR: task with public_id {payload['public_id']} does not exist (yet?)")
                    print(f"event: {record_data}")

            elif (record_data["event_name"] == "tasks.task-reassigned") & (str(record_data["event_version"]) == "1"):
                if BillingTask.objects.filter(public_id=payload["public_id"]).exists():
                    task = BillingTask.objects.get(public_id=payload["public_id"])
                    task.assignee_public_id = payload["new_assignee_public_id"]
                else:
                    task = BillingTask(
                        public_id=payload["public_id"],
                        created=payload["created"],
                        assignee_public_id=payload["new_assignee_public_id"],
                        title=payload.get("title"),
                        status=payload.get("status"),
                    )
                task.save()
                print(f"re-assigned task {task} to user {payload['new_assignee_public_id']}")

            elif (record_data["event_name"] == "users.user-created") & (str(record_data["event_version"]) == "1"):
                user = BillingUser(
                    public_id=payload["public_id"],
                    created=payload["created"],
                    role=payload["user_role"],
                    first_name=payload["first_name"],
                    last_name=payload["last_name"],
                )
                user.save()
                print(f"created BillingUser with pub_id {user} and role {user}")

            elif (record_data["event_name"] == "users.user-updated") & (str(record_data["event_version"]) == "1"):
                user = BillingUser.objects.get(public_id=payload["public_id"])
                user.role = payload["user_role"]
                user.first_name = payload["first_name"]
                user.last_name = payload["last_name"]
                user.save()
                print(f"updated BillingUser with pub_id {user.public_id}")

            else:
                print(f"ignoring message with key `{record_key}` and meta `{record_data}`")

        except IntegrityError as e:
            print(f"seems already consumed event with key `{record_key}` and meta `{record_data}`")

        except Exception as e:
            # DLQ for failed messages
            event_seen = record_data.get("event_seen_times", 0)
            record_data.update(
                {
                    "event_seen_times": event_seen + 1,
                    "last_error": str(e),
                }
            )
            p.produce(topic=Topics.billing_dlq, key=record_data["event_id"], value=record_data)
            # TODO add DLQ consumer logic (somewhere?)

            if DEBUG:
                print(f"\n\t >>> ERROR processing message with key `{record_key}` and meta `{record_data}`\n\n {e}\n")
                raise e
            else:
                # ACK the message to avoid re-processing
                self.commit()


consumer = BillingTaskConsumer(group_id="billing_consumer")
consumer.subscribe(
    [
        Topics.tasks_stream,
        Topics.tasks,
        Topics.users_stream,
    ]
)


def start_billing_consumer():
    consumer.start_consuming(timeout=5.0)
