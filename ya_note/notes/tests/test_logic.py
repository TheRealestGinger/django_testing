from http import HTTPStatus

from pytils.translit import slugify

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
    NOTES_ADD_REDIRECT_URL
)
from notes.forms import WARNING
from notes.models import Note


class TestLogic(Base):
    def test_user_can_create_note(self):
        Note.objects.all().delete()
        self.assertRedirects(
            self.author_client.post(NOTES_ADD_URL, data=self.form_data),
            NOTES_SUCCESS_URL
        )
        new_note = Note.objects.get()
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        self.assertRedirects(
            self.client.post(NOTES_ADD_URL, data=self.form_data),
            NOTES_ADD_REDIRECT_URL
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        notes = Note.objects.all()
        self.form_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(NOTES_ADD_URL, data=self.form_data),
            'form',
            'slug',
            errors=(self.note.slug + WARNING))
        self.assertEqual(set(notes), set(Note.objects.all()))

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        self.assertRedirects(
            self.author_client.post(NOTES_ADD_URL, data=self.form_data),
            NOTES_SUCCESS_URL
        )
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(
            new_note.slug,
            slugify(self.form_data['title'])
        )
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        self.assertRedirects(
            self.author_client.post(NOTES_EDIT_URL, data=self.form_data),
            NOTES_SUCCESS_URL
        )
        note = Note.objects.get(pk=self.note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.other_author_client.post(
            NOTES_EDIT_URL,
            data=self.form_data
        ).status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(pk=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        self.assertRedirects(
            self.author_client.post(NOTES_DELETE_URL),
            NOTES_SUCCESS_URL
        )
        self.assertNotIn(self.note, Note.objects.all())

    def test_user_cant_delete_note_of_another_user(self):
        self.assertEqual(
            self.other_author_client.post(NOTES_DELETE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        note_from_db = Note.objects.get(pk=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)
