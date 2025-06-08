import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from materials.models import Course, Subscription
from users.models import User

logger = logging.getLogger(__name__)


@shared_task
def course_update(course_pk):
    course = Course.objects.filter(pk=course_pk).first()
    users = User.objects.all()
    for user in users:
        subscription = Subscription.objects.filter(
            course=course_pk, user=user.pk
        ).first()
        if subscription:
            send_mail(
                subject=f'У нас обновление курса "{course.title}"',
                message=f'Добрый день! Курс "{course.title}" обновился!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )


@shared_task
def check_last_login():
    users = User.objects.filter(last_login__isnull=False, is_active=True)
    deactivated_users = []

    for user in users:
        if timezone.now() - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            deactivated_users.append(user.email)
            logger.info(f"Пользователь {user.email} заблокирован")
        else:
            logger.info(f"Пользователь {user.email} в сети")

    if deactivated_users:
        return f'Заблокированы пользователи: {", ".join(deactivated_users)}'
    else:
        return "Нет пользователей для блокировки"
