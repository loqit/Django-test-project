import pytest
from django.contrib.auth.models import User

from dj_test.apps.main_page.models import Article, Comment


@pytest.fixture
def user_factory(db):
    def create_user(username='TestUser', password='TestPassword', email='test@mail.ru'):
        if User.objects.filter(username=username).exists():
            return User.objects.filter(username=username).first()
        else:
            user = User.objects.create(username=username, password=password, email=email)
            return user

    return create_user


@pytest.fixture
def article_factory(db):
    def create_article(article_title='article_title', article_text='article_text'):
        if Article.objects.filter(article_text=article_text).exists():
            return Article.objects.filter(article_text=article_text).first()
        else:
            article = Article.objects.create(article_title=article_title, article_text=article_text)
            return article

    return create_article


def test_user_data(db, user_factory):
    user = user_factory(username='testUser', password='123456', email='test@mail.ru')
    assert user.username == 'testUser' and user.password == '123456' and user.email == 'test@mail.ru'


def test_user_permissions(db, user_factory):
    user = user_factory(username='testUser', password='123456', email='test@mail.ru')
    assert user.is_superuser == False


@pytest.fixture
def profile_factory(db, user_factory):
    def create_profile(voted=False):
        user = user_factory()
        user.profile.is_voted = voted
        user.save()

        return user.profile

    return create_profile


@pytest.fixture
def comment_factory(db):
    def create_comment(user=None, article=None, text='some_comment'):
        if Comment.objects.filter(comment_text=text).exists():
            return Comment.objects.filter(comment_text=text and article == article).first()
        else:
            return Comment.objects.create(author_name=user, comment_text=text, article=article)

    return create_comment


def test_article_str(db, article_factory):
    article = article_factory(article_title='title', article_text='test123')
    assert str(article) == 'title test123'


def test_articles_equal(db, article_factory):
    article = article_factory(article_title='test', article_text='test123')
    article1 = article_factory(article_title='test', article_text='test123')

    assert article1 == article


def test_articles_not_equal(db, article_factory):
    article = article_factory(article_title='test', article_text='test123')
    article1 = article_factory(article_title='test', article_text='test12')

    assert not article1 == article


def test_comment_user(db, comment_factory, user_factory, article_factory):
    user = user_factory()
    article = article_factory()
    comment = comment_factory(user=user, article=article, text='some text')
    assert comment.author_name.is_anonymous == False


def test_comment_str(db, comment_factory, user_factory, article_factory):
    user = user_factory()
    article = article_factory()
    comment = comment_factory(user=user, article=article, text='some text')
    assert str(comment) == comment.comment_text


'''
def test_comment_text(db, comment_factory, user_factory, candidate_factory):
    user = user_factory()
    candidate = candidate_factory()
    comment = comment_factory(user=user, candidate=candidate, text='some text')

    assert comment.text == 'some text'
'''
