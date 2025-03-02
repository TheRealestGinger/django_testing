from http import HTTPStatus

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Коммент'}
BAD_WORD_COMMENT = {'text': f'Какой-то текст, {BAD_WORDS}, еще текст'}


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


def test_user_cant_use_bad_words(author_client, news_detail_url):
    assertFormError(
        author_client.post(
            news_detail_url,
            data=BAD_WORD_COMMENT
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
):
    assert (not_author_client.post(comment_delete_url).status_code
            == HTTPStatus.NOT_FOUND)
    assert Comment.objects.count() == 1
    old_comment = Comment.objects.get(pk=comment.id)
    assert old_comment.text == comment.text
    assert old_comment.news == comment.news
    assert old_comment.author == comment.author


def test_author_can_edit_comment(
    author_client,
    comment,
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
    new_comment = Comment.objects.get(pk=comment.id)
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news == comment.news
    assert new_comment.author == comment.author


def test_user_cant_edit_comment_of_another_user(
    not_author_client,
    comment,
    comment_edit_url
):
    assert not_author_client.post(
        comment_edit_url,
        data=FORM_DATA
    ).status_code == HTTPStatus.NOT_FOUND
    old_comment = Comment.objects.get(pk=comment.id)
    assert old_comment.text == comment.text
    assert old_comment.news == comment.news
    assert old_comment.author == comment.author
