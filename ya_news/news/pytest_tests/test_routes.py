from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


HOME_URL = pytest.lazy_fixture('home_url')
NEWS_DETAIL_URL = pytest.lazy_fixture('news_detail_url')
USERS_LOGIN_URL = pytest.lazy_fixture('users_login_url')
USERS_LOGOUT_URL = pytest.lazy_fixture('users_logout_url')
USERS_SIGNUP_URL = pytest.lazy_fixture('users_signup_url')
COMMENT_EDIT_URL = pytest.lazy_fixture('comment_edit_url')
COMMENT_DELETE_URL = pytest.lazy_fixture('comment_delete_url')
CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')


@pytest.mark.parametrize(
    'url, user, status',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK),
        (NEWS_DETAIL_URL, CLIENT, HTTPStatus.OK),
        (USERS_LOGIN_URL, CLIENT, HTTPStatus.OK),
        (USERS_LOGOUT_URL, CLIENT, HTTPStatus.OK),
        (USERS_SIGNUP_URL, CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (COMMENT_EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (COMMENT_DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND)
    )
)
def test_pages_availability(url, user, status):
    assert user.get(url).status_code == status


@pytest.mark.parametrize(
    'url',
    (
        COMMENT_EDIT_URL,
        COMMENT_DELETE_URL
    )
)
def test_redirect_for_anonymous_client(client, url, redirect_url):
    assertRedirects(client.get(url), redirect_url + url)
