# Generated by Django 4.1.6 on 2023-02-21 02:24

import ckeditor_uploader.fields
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
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="nome")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="descrição"),
                ),
            ],
            options={
                "verbose_name": "categoria",
                "verbose_name_plural": "categorias",
            },
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="nome")),
                ("summary", models.TextField(verbose_name="resumo")),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="descrição"
                    ),
                ),
                ("duration", models.DurationField(verbose_name="duração")),
                ("availability", models.DurationField(verbose_name="prazo")),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="course_images",
                        verbose_name="imagem do curso",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, verbose_name="preço"
                    ),
                ),
                (
                    "intro_video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="intro_videos",
                        verbose_name="video introdutório",
                    ),
                ),
                (
                    "intro_video_id",
                    models.URLField(
                        blank=True, null=True, verbose_name="URL do video introdutório"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="data de criação"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="courses.category",
                        verbose_name="categoria",
                    ),
                ),
            ],
            options={
                "verbose_name": "curso",
                "verbose_name_plural": "cursos",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="nome")),
                ("summary", models.TextField(verbose_name="resumo")),
                (
                    "description",
                    ckeditor_uploader.fields.RichTextUploadingField(
                        verbose_name="descrição"
                    ),
                ),
                ("duration", models.DurationField(verbose_name="duração")),
                (
                    "video",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="lesson_videos",
                        verbose_name="video da aula",
                    ),
                ),
                (
                    "video_id",
                    models.URLField(
                        blank=True, null=True, verbose_name="URL do video da aula"
                    ),
                ),
            ],
            options={
                "verbose_name": "aula",
                "verbose_name_plural": "aulas",
            },
        ),
        migrations.CreateModel(
            name="WatchedLesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="courses.lesson"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watched_lessons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="nome")),
                ("summary", models.TextField(verbose_name="resumo")),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sections",
                        to="courses.course",
                        verbose_name="curso",
                    ),
                ),
            ],
            options={
                "verbose_name": "seção",
                "verbose_name_plural": "seções",
            },
        ),
        migrations.CreateModel(
            name="PurchasedCourse",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="courses.course"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchased_courses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="lesson",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lessons",
                to="courses.section",
                verbose_name="seção",
            ),
        ),
    ]
