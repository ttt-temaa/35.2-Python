from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название курса")
    preview = models.ImageField(verbose_name="Фотография", blank=True, null=True)
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(
        max_length=200, verbose_name="Описание курса", blank=True, null=True
    )
    preview = models.ImageField(verbose_name="Фотография", blank=True, null=True)
    video_link = models.TextField(
        max_length=200, verbose_name="Ссылка на видео", blank=True, null=True
    )

    course = models.ForeignKey(
        Course, related_name="lessons", null=True, blank=True, on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец курса",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    subscription_sign = models.BooleanField(
        default=False, verbose_name="Признак подписки"
    )

    def __str__(self):
        return f"{self.user} {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
