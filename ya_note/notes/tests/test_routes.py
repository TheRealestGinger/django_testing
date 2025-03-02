from http import HTTPStatus

from .conftest import Base


class TestRoutes(Base):
    def test_pages_availability(self):
        for url, user, status in (
            (self.NOTES_HOME, self.client, HTTPStatus.OK),
            (self.LOGIN_URL, self.client, HTTPStatus.OK),
            (self.LOGOUT_URL, self.client, HTTPStatus.OK),
            (self.SIGNUP_URL, self.client, HTTPStatus.OK),
            (self.NOTES_LIST_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_ADD_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_SUCCESS_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_DETAIL_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_EDIT_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_DELETE_URL, self.author_client, HTTPStatus.OK),
            (
                self.NOTES_DETAIL_URL,
                self.other_author_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                self.NOTES_EDIT_URL,
                self.other_author_client,
                HTTPStatus.NOT_FOUND
            ),
            (
                self.NOTES_DELETE_URL,
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
            self.NOTES_LIST_URL,
            self.NOTES_SUCCESS_URL,
            self.NOTES_ADD_URL,
            self.NOTES_DETAIL_URL,
            self.NOTES_EDIT_URL,
            self.NOTES_DELETE_URL
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    self.REDIRECT_URL+url
                )
