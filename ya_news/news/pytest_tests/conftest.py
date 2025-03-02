from datetime import datetime, timedelta

from django.test.client import Client
from django.conf import settings
from django.urls import reverse
import pytest

from news.models import Comment, News


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_detail_url(comment):
    return reverse('news:detail', args=(comment.id,))


@pytest.fixture
def comment_url(news_detail_url):
    return news_detail_url + '#comments'


@pytest.fixture
def comment_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def users_login_url():
    return reverse('users:login')


@pytest.fixture
def users_logout_url():
    return reverse('users:logout')


@pytest.fixture
def users_signup_url():
    return reverse('users:signup')


@pytest.fixture
def redirect_url(users_login_url):
    return f'{users_login_url}?next='


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news():
    return News.objects.create(
        title='Заголовок',
        text='Текст заметки'
    )


@pytest.fixture
def news11():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
        text='Текст',
        news=news,
        author=author
    )


@pytest.fixture
def comment11(news, author):
    today = datetime.today()
    Comment.objects.bulk_create(
        Comment(
            text='Просто текст.',
            news=news,
            author=author,
            created=today - timedelta(days=index)
        )
        for index in range(11)
    )
