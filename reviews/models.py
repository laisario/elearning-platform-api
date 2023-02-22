from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from courses.models import Course


class Review(models.Model):
    title = models.CharField(_('título'), max_length=30)
    description = models.TextField(_('descrição'), blank=True, null=True)
    rating = models.IntegerField(_('nota'),
                                 default=5,
                                 validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")

    class Meta:
        verbose_name = _('avaliação')
        verbose_name_plural = _('avaliações')


class Testimonial(models.Model):
    title = models.CharField(_('título'), max_length=30)
    description = models.TextField(_('descrição'), blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('testemunho')
        verbose_name_plural = _('testemunhos')
