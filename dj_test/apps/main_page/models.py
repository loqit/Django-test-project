from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Article(models.Model):
    article_title = models.CharField('Название статьи', max_length=200)
    article_text = models.TextField('Текст статьи')
    pub_date = models.DateTimeField('Время публикации', default=timezone.now())
    author_name = models.CharField('name', max_length=50, default='')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.article_title + ' ' + self.article_text


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_text = models.CharField('comment', max_length=200)
    author_name = models.CharField('name', max_length=50)
    pub_date = models.DateTimeField('Время публикации', default=timezone.now())

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment_text


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_verified = models.BooleanField(verbose_name='Подтверждён', default=False)
    is_voted = models.BooleanField(verbose_name='Проголосовал', default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not Profile.objects.filter(user=instance).exists():
        create_user_profile(sender, instance, created=True)
    instance.profile.save()
