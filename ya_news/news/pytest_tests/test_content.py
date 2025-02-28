import pytest

from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm

HOME_URL = reverse('news:home')


@pytest.mark.django_db
def test_news_count(client, news11):
    news_count = client.get(HOME_URL).context['object_list'].count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, news11):
    all_dates = [
        news.date for news in client.get(HOME_URL).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.django_db
def test_comments_order(client, comment, news):
    response = client.get(reverse('news:detail', args=(news.id,)))
    assert 'news' in response.context
    news = response.context['news']
    all_timestamps = [comment.created for comment in news.comment_set.all()]
    assert all_timestamps == sorted(all_timestamps)


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, comment):
    response = client.get(reverse('news:detail', args=(comment.id,)))
    assert 'form' not in response.context


@pytest.mark.django_db
def test_authorized_client_has_form(author_client, comment):
    response = author_client.get(reverse('news:detail', args=(comment.id,)))
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
