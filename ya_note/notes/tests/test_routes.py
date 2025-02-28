from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )

    def test_pages_availability(self):
        for name in (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup'
        ):
            with self.subTest(name=name):
                self.assertEqual(
                    self.client.get(reverse(name)).status_code,
                    HTTPStatus.OK
                )

    def test_pages_availability_for_auth_client(self):
        self.client.force_login(self.reader)
        for name in (
            'notes:list',
            'notes:add',
            'notes:success'
        ):
            with self.subTest(name=name):
                self.assertEqual(
                    self.client.get(reverse(name, args=None)).status_code,
                    HTTPStatus.OK
                )

    def test_availability_for_detail_edit_and_delete(self):
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (
                'notes:detail',
                'notes:edit',
                'notes:delete'
            ):
                with self.subTest(user=user, name=name):
                    self.assertEqual(self.client.get(
                        reverse(
                            name,
                            args=(self.note.slug,)
                        )).status_code,
                        status
                    )

    def test_redirects_for_anonymous_client(self):
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,))
        )
        login_url = reverse('users:login')
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                self.assertRedirects(
                    self.client.get(url),
                    f'{login_url}?next={url}'
                )
