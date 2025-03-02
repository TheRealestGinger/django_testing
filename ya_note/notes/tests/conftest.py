from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.other_author = User.objects.create(username='Другой автор')
        cls.other_author_client = Client()
        cls.other_author_client.force_login(cls.other_author)
        cls.note = Note.objects.create(
            title='Заголовок автора',
            text='Текст',
            author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug',
            'author': cls.author
        }
        cls.NOTES_HOME = reverse('notes:home')
        cls.NOTES_SUCCESS_URL = reverse('notes:success')
        cls.NOTES_LIST_URL = reverse('notes:list')
        cls.NOTES_ADD_URL = reverse('notes:add')
        cls.NOTES_DETAIL_URL = reverse('notes:detail', args=(cls.note.slug,))
        cls.NOTES_EDIT_URL = reverse('notes:edit', args=(cls.note.slug,))
        cls.NOTES_DELETE_URL = reverse('notes:delete', args=(cls.note.slug,))
        cls.LOGIN_URL = reverse('users:login')
        cls.LOGOUT_URL = reverse('users:logout')
        cls.SIGNUP_URL = reverse('users:signup')
        cls.REDIRECT_URL = f'{cls.LOGIN_URL}?next='
