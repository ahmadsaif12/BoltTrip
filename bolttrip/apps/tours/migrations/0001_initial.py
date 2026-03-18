from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TourType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=80, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("icon_url", models.URLField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tours_tourtype_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tours_tourtype_updated", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="TourPackage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=180)),
                ("slug", models.SlugField(blank=True, max_length=200, unique=True)),
                ("short_description", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("destination", models.CharField(max_length=120)),
                ("country", models.CharField(max_length=120)),
                ("duration_days", models.PositiveSmallIntegerField(default=1)),
                ("duration_nights", models.PositiveSmallIntegerField(default=0)),
                ("group_size", models.PositiveSmallIntegerField(default=1)),
                ("rating", models.DecimalField(decimal_places=1, default=0.0, max_digits=2)),
                ("review_count", models.PositiveIntegerField(default=0)),
                ("base_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("discounted_price", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("currency", models.CharField(default="USD", max_length=10)),
                ("cover_image_url", models.URLField()),
                ("gallery_image_urls", models.JSONField(blank=True, default=list)),
                ("highlights", models.JSONField(blank=True, default=list)),
                ("includes", models.JSONField(blank=True, default=list)),
                ("excludes", models.JSONField(blank=True, default=list)),
                ("is_featured", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tours_tourpackage_created", to=settings.AUTH_USER_MODEL)),
                ("package_type", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="packages", to="tours.tourtype")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tours_tourpackage_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["sort_order", "-created_at"],
            },
        ),
    ]
