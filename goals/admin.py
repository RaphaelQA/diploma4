from django.contrib import admin

from goals.models import GoalCategory, Goal, Comment


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user.username")


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user.username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "user", "created", "updated")
    search_fields = ("text", "user.username")

