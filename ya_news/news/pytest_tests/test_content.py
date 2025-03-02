from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_news_count(client, news11, home_url):
    assert (client.get(home_url).context['object_list'].count()
            == settings.NEWS_COUNT_ON_HOME_PAGE)


def test_news_order(client, news11, home_url):
    all_dates = [
        news.date for news in client.get(home_url).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comments_order(client, comment11, news, news_detail_url):
    response = client.get(news_detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_timestamps = [comment.created for comment in news.comment_set.all()]
    assert all_timestamps == sorted(all_timestamps)


def test_anonymous_client_has_no_form(client, comment_detail_url):
    assert ('form' not in client.get(comment_detail_url).context)


def test_authorized_client_has_form(author_client, comment_detail_url):
    assert isinstance(
        author_client.get(comment_detail_url).context.get('form'), CommentForm
    )
