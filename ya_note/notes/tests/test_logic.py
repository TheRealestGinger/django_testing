from http import HTTPStatus

from pytils.translit import slugify

from .conftest import Base
from notes.forms import WARNING
from notes.models import Note


class TestLogic(Base):
    def test_user_can_create_note(self):
        Note.objects.all().delete()
        self.assertRedirects(
            self.author_client.post(self.NOTES_ADD_URL, data=self.form_data),
            self.NOTES_SUCCESS_URL
        )
        new_note = Note.objects.get()
        self.assertEqual(Note.objects.count(), 1)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        self.assertRedirects(
            self.client.post(self.NOTES_ADD_URL, data=self.form_data),
            self.REDIRECT_URL+self.NOTES_ADD_URL
        )
        self.assertEqual(Note.objects.count(), 0)

    def test_not_unique_slug(self):
        notes = Note.objects.all()
        self.form_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(self.NOTES_ADD_URL, data=self.form_data),
            'form',
            'slug',
            errors=(self.note.slug + WARNING))
        self.assertQuerysetEqual(notes, Note.objects.all())

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        self.assertRedirects(
            self.author_client.post(self.NOTES_ADD_URL, data=self.form_data),
            self.NOTES_SUCCESS_URL
        )
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(
            new_note.slug,
            slugify(self.form_data['title'])
        )
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.form_data['author'])

    def test_author_can_edit_note(self):
        self.assertRedirects(
            self.author_client.post(self.NOTES_EDIT_URL, data=self.form_data),
            self.NOTES_SUCCESS_URL
        )
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.form_data['author'])

    def test_user_cant_edit_note_of_another_user(self):
        self.assertEqual(self.other_author_client.post(
            self.NOTES_EDIT_URL,
            data=self.form_data
        ).status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get()
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        note = Note.objects.get()
        self.assertRedirects(
            self.author_client.post(self.NOTES_DELETE_URL),
            self.NOTES_SUCCESS_URL
        )
        self.assertNotIn(note, Note.objects.all())

    def test_user_cant_delete_note_of_another_user(self):
        self.assertEqual(
            self.other_author_client.post(self.NOTES_DELETE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        note_from_db = Note.objects.get()
        self.assertIn(note_from_db, Note.objects.all())
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)
