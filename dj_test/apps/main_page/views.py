from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from .models import Article, Comment
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse


def index(request):
    latest_news = Article.objects.order_by('-pub_date')[:5]
    return render(request, 'arcticles/list.html', {'latest_news': latest_news})


def detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    l = article.comment_set.order_by('-id')[:10]
    return render(request, 'arcticles/detail.html', {'article': article, 'l': l})


def leave_comment(request, article_id):
    a = get_object_or_404(Article, id=article_id)
    a.comment_set.create(author_name=request.POST['name'], comment_text=request.POST['text'])
    return HttpResponseRedirect(reverse('main_page:detail', args=(a.id,)))


def create_article(request):

    Article.objects.create(article_title=request.POST.get('name'), article_text=request.POST.get('text'), pub_date=timezone.now())
    return HttpResponseRedirect(reverse('main_page:index'))



def home(request):
    return render(request, 'arcticles/home.html')
