from django.db import models


class GalleryCategory(models.Model):
    name = models.CharField(
        max_length=100
    )  # e.g. Wedding, Corporate, Birthday
    slug = models.SlugField(unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    title = models.CharField(
        max_length=150, blank=True, help_text="Optional Title/Caption"
    )
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="gallery/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"