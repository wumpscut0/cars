from django.contrib import admin

from .models import Car, Comment


@admin.register(Car)
class CarModelAdmin(admin.ModelAdmin):
    description_display_limit = 42
    make_display_limit = 10
    model_display_limit = 10
    list_display = (
        "pk",
        "owner",
        "created_at",
        "updated_at",
        "make_short",
        "model_short",
        "year",
        "description_short",
    )

    @admin.display(empty_value="No description")
    def description_short(self, obj: Car):
        if len(obj.description) < self.description_display_limit:
            return obj.description
        return obj.description[: self.description_display_limit] + "..."

    @admin.display()
    def make_short(self, obj: Car):
        if len(obj.make) < self.make_display_limit:
            return obj.make
        return obj.description[: self.make_display_limit] + "..."

    @admin.display()
    def model_short(self, obj: Car):
        if len(obj.model) < self.model_display_limit:
            return obj.model
        return obj.description[: self.model_display_limit] + "..."


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    content_display_limit = 42
    list_display = "pk", "car", "author", "created_at", "content_short"
    list_display_links = "car", "content_short"

    def content_short(self, obj: Comment):
        if len(obj.content) < self.content_display_limit:
            return obj.content
        return obj.content[: self.content_display_limit] + "..."
