from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from ordered_model.models import OrderedModel

from core.storages import PublicMediaStorage

class Category(models.Model):
    name = models.CharField(_('nome'), max_length=30)
    description = models.TextField(_('descrição'), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('categoria')
        verbose_name_plural = _('categorias')


class Course(models.Model):
    name = models.CharField(_('nome'), max_length=30)
    summary = models.TextField(_('resumo'))
    description = RichTextField(_('descrição'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('categoria'))
    duration = models.DurationField(_('duração'))
    availability = models.DurationField(_('prazo'))
    image = models.ImageField(_('imagem do curso'), storage=PublicMediaStorage(), null=True, blank=True)
    price = models.DecimalField(_('preço'), decimal_places=2, max_digits=12)
    intro_video = models.FileField(_('video introdutório'), storage=PublicMediaStorage(), null=True, blank=True)
    intro_video_id = models.URLField(_('URL do video introdutório'), null=True, blank=True)
    created_at = models.DateTimeField(_('data de criação'), auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('curso')
        verbose_name_plural = _('cursos')


class Section(OrderedModel):
    name = models.CharField(_('nome'), max_length=30)
    summary = models.TextField(_('resumo'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections', verbose_name=_('curso'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('seção')
        verbose_name_plural = _('seções')


class Lesson(OrderedModel):
    name = models.CharField(_('nome'), max_length=30)
    summary = models.TextField(_('resumo'))
    description = RichTextField(_('descrição'))
    duration = models.DurationField(_('duração'))
    video = models.FileField(_('video da aula'), storage=PublicMediaStorage(), null=True, blank=True)
    video_id = models.URLField(_('URL do video da aula'), null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lessons', verbose_name=_('seção'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('aula')
        verbose_name_plural = _('aulas')


class PurchasedCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchased_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class WatchedLesson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watched_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)