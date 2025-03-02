from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from notes.models import Note

User = get_user_model()

SLUG = 'slug'
NOTES_HOME = reverse('notes:home')
NOTES_SUCCESS_URL = reverse('notes:success')
NOTES_LIST_URL = reverse('notes:list')
NOTES_ADD_URL = reverse('notes:add')
NOTES_DETAIL_URL = reverse('notes:detail', args=(SLUG,))
NOTES_EDIT_URL = reverse('notes:edit', args=(SLUG,))
NOTES_DELETE_URL = reverse('notes:delete', args=(SLUG,))
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
NOTES_EDIT_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_EDIT_URL}'
NOTES_DELETE_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_DELETE_URL}'
NOTES_LIST_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_LIST_URL}'
NOTES_ADD_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_ADD_URL}'
NOTES_DETAIL_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_DETAIL_URL}'
NOTES_SUCCESS_REDIRECT_URL = f'{LOGIN_URL}?next={NOTES_SUCCESS_URL}'


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
            slug=SLUG,
            author=cls.author
        )
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug',
        }
