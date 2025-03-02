from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Коммент'}


def test_anonymous_user_cant_create_comment(client, news_detail_url):
    client.post(news_detail_url, data=FORM_DATA)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author_client,
    author, news,
    news_detail_url,
    comment_url
):
    assertRedirects(
        author_client.post(news_detail_url, data=FORM_DATA), comment_url
    )
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
        'bad_words',
        BAD_WORDS
)
def test_user_cant_use_bad_words(author_client, news_detail_url, bad_words):
    assertFormError(
        author_client.post(
            news_detail_url,
            data={'text': f'Какой-то текст, {bad_words}, еще текст'}
        ),
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(
    author_client,
    comment_delete_url,
    comment_url
):
    assertRedirects(
        author_client.post(comment_delete_url),
        comment_url
    )
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(
    not_author_client,
    comment_delete_url,
    comment,
    news,
    author
):
    assert (not_author_client.post(comment_delete_url).status_code
            == HTTPStatus.NOT_FOUND)
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment.text
    assert comment.news == news
    assert comment.author == author


def test_author_can_edit_comment(
    author_client,
    comment,
    news,
    author,
    comment_edit_url,
    comment_url
):
    assertRedirects(
        author_client.post(
            comment_edit_url,
            data=FORM_DATA
        ),
        comment_url
    )
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    comment,
    news,
    author,
    comment_edit_url
):
    assert not_author_client.post(
        comment_edit_url,
        data=FORM_DATA
    ).status_code == HTTPStatus.NOT_FOUND
    comment = Comment.objects.get()
    assert comment.text != FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author
