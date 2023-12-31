from typing import Tuple
from django.core.validators import MinLengthValidator
from django.db import models
from core.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    class Meta:
        abstract = True


class Board(BaseModel):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(BaseModel):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )


class GoalCategory(BaseModel):
    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255, validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> models.CharField:
        return self.title


class Goal(BaseModel):

    class Status(models.IntegerChoices):
        to_do: Tuple[int, str] = 1, 'К выполнению'
        in_progress: Tuple[int, str] = 2, 'В процессе'
        done: Tuple[int, str] = 3, 'Выполнено'
        archived: Tuple[int, str] = 4, 'Архивировано'

    class Priority(models.IntegerChoices):
        low: Tuple[int, str] = 1, 'Низкий'
        medium: Tuple[int, str] = 2, 'Средний'
        high: Tuple[int, str] = 3, 'Высокий'
        critical: Tuple[int, str] = 4, 'Критический'

    title = models.CharField(verbose_name="Название", max_length=255, validators=[MinLengthValidator(1)])
    description = models.TextField(verbose_name="Описание", max_length=255, null=True, blank=True)
    category = models.ForeignKey(
        verbose_name="Категория", to=GoalCategory, on_delete=models.CASCADE, related_name='goals'
    )
    due_date = models.DateTimeField(verbose_name="Дата выполнения", null=True, blank=True)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.to_do)
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет", choices=Priority.choices, default=Priority.medium
    )

    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    def __str__(self) -> models.CharField:
        return self.title


class Comment(BaseModel):
    text = models.CharField(verbose_name="Текст", max_length=255, validators=[MinLengthValidator(1)])
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    goal = models.ForeignKey(
        verbose_name="Цель", to=Goal, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
