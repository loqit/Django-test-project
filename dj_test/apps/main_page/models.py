from django.db import models


# Create your models here.
class Article(models.Model):
    article_title = models.CharField('Название статьи', max_length=200)
    article_text = models.TextField('Текст статьи')
    pub_date = models.DateTimeField('Время публикации')


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_text = models.CharField('comment', max_length=200)
    
    author_name = models.CharField('name', max_length=50)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.author_name
