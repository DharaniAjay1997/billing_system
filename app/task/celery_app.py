from celery import Celery

celery = Celery(
    "billing_system",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend="rpc://",
    include=[
        "app.task.email_task",
    ],
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)