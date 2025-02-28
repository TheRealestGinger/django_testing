from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.other_author = User.objects.create(username='Другой автор')
        cls.note = Note.objects.create(
            title='Заголовок автора',
            text='Текст',
            author=cls.author
        )

    def test_notes_list_for_different_users(self):
        users_statuses = (
            (self.author, self.assertIn),
            (self.other_author, self.assertNotIn),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            status(
                self.note,
                self.client.get(reverse('notes:list')).context['object_list']
            )

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        for name, args in (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,))
        ):
            with self.subTest(name=name):
                response = self.client.get(reverse(name, args=args))
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
