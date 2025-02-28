from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.author_note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug='slug',
            author=cls.user
        )
        cls.note = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.note)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 2)
        new_note = Note.objects.get(slug=self.note['slug'])
        self.assertEqual(new_note.title, self.note['title'])
        self.assertEqual(new_note.text, self.note['text'])
        self.assertEqual(new_note.slug, self.note['slug'])
        self.assertEqual(new_note.author, self.user)

    def test_anonymous_user_cant_create_note(self):
        login_url = reverse('users:login')
        self.assertRedirects(
            self.client.post(self.url, data=self.note),
            f'{login_url}?next={self.url}'
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_not_unique_slug(self):
        self.note['slug'] = self.author_note.slug
        self.assertFormError(
            self.auth_client.post(self.url, data=self.note),
            'form',
            'slug',
            errors=(self.author_note.slug + WARNING))
        self.assertEqual(Note.objects.count(), 1)

    def test_empty_slug(self):
        self.note.pop('slug')
        self.assertRedirects(
            self.auth_client.post(self.url, data=self.note),
            reverse('notes:success')
        )
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(
            Note.objects.get(slug=slugify(self.note['title'])).slug,
            slugify(self.note['title'])
        )


class TestNoteEditDelete(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    def test_author_can_edit_note(self):
        self.assertRedirects(
            self.author_client.post(self.edit_url, data=self.form_data),
            reverse('notes:success')
        )
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.reader_client.post(
            self.edit_url,
            data=self.form_data
        ).status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(slug=self.note.slug)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        self.assertRedirects(
            self.author_client.post(self.delete_url),
            reverse('notes:success')
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cant_delete_note_of_another_user(self):
        self.assertEqual(
            self.reader_client.post(self.delete_url).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(Note.objects.count(), 1)
