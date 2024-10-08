from celery import shared_task


@shared_task
def test():
    print("Working celery")

@shared_task
def send_mail(user):
    # user.email()
    pass