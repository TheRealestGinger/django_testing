from http import HTTPStatus

from .conftest import (
    Base,
    NOTES_HOME,
    NOTES_SUCCESS_URL,
    NOTES_LIST_URL,
    NOTES_ADD_URL,
    NOTES_DETAIL_URL,
    NOTES_EDIT_URL,
    NOTES_DELETE_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    NOTES_EDIT_REDIRECT_URL,
    NOTES_DELETE_REDIRECT_URL,
    NOTES_LIST_REDIRECT_URL,
    NOTES_ADD_REDIRECT_URL,
    NOTES_DETAIL_REDIRECT_URL,
    NOTES_SUCCESS_REDIRECT_URL
)


class TestRoutes(Base):
    def test_pages_availability(self):
        for url, user, status in (
            (NOTES_HOME, self.client, HTTPStatus.OK),
            (LOGIN_URL, self.client, HTTPStatus.OK),
            (LOGOUT_URL, self.client, HTTPStatus.OK),
            (SIGNUP_URL, self.client, HTTPStatus.OK),
            (NOTES_LIST_URL, self.author_client, HTTPStatus.OK),
            (NOTES_ADD_URL, self.author_client, HTTPStatus.OK),
            (NOTES_SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (NOTES_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (NOTES_EDIT_URL, self.author_client, HTTPStatus.OK),
            (NOTES_DELETE_URL, self.author_client, HTTPStatus.OK),
            (NOTES_LIST_REDIRECT_URL, self.client, HTTPStatus.OK),
            (NOTES_ADD_REDIRECT_URL, self.client, HTTPStatus.OK),
            (NOTES_SUCCESS_REDIRECT_URL, self.client, HTTPStatus.OK),
            (NOTES_DETAIL_REDIRECT_URL, self.client, HTTPStatus.OK),
            (NOTES_EDIT_REDIRECT_URL, self.client, HTTPStatus.OK),
            (NOTES_DELETE_REDIRECT_URL, self.client, HTTPStatus.OK),
            (NOTES_LIST_URL, self.client, HTTPStatus.FOUND),
            (NOTES_ADD_URL, self.client, HTTPStatus.FOUND),
            (NOTES_SUCCESS_URL, self.client, HTTPStatus.FOUND),
            (NOTES_DETAIL_URL, self.client, HTTPStatus.FOUND),
            (NOTES_EDIT_URL, self.client, HTTPStatus.FOUND),
            (NOTES_DELETE_URL, self.client, HTTPStatus.FOUND),
            (
                NOTES_DETAIL_URL,
                self.other_author_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                NOTES_EDIT_URL,
                self.other_author_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                NOTES_DELETE_URL,
                self.other_author_client,
                HTTPStatus.NOT_FOUND
            ),
        ):
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual(
                    user.get(url).status_code,
                    status
                )

    def test_redirects_for_anonymous_client(self):
        urls = (
            (NOTES_LIST_URL, NOTES_LIST_REDIRECT_URL),
            (NOTES_SUCCESS_URL, NOTES_SUCCESS_REDIRECT_URL),
            (NOTES_ADD_URL, NOTES_ADD_REDIRECT_URL),
            (NOTES_DETAIL_URL, NOTES_DETAIL_REDIRECT_URL),
            (NOTES_EDIT_URL, NOTES_EDIT_REDIRECT_URL),
            (NOTES_DELETE_URL, NOTES_DELETE_REDIRECT_URL)
        )
        for url, redirect_url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url
                )
