from .conftest import (
    Base,
    NOTES_LIST_URL,
    NOTES_ADD_URL,
    NOTES_EDIT_URL,
)

from notes.models import Note
from notes.forms import NoteForm


class TestContent(Base):
    def test_notes_list_for_author(self):
        notes = self.author_client.get(
            NOTES_LIST_URL
        ).context['object_list']
        self.assertIn(
            self.note,
            notes
        )
        note = Note.objects.get(pk=self.note.id)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)

    def test_notes_list_for_not_author(self):
        self.assertNotIn(
            self.note,
            self.other_author_client.get(
                NOTES_LIST_URL
            ).context['object_list']
        )

    def test_authorized_client_has_form(self):
        for name in (
            NOTES_ADD_URL,
            NOTES_EDIT_URL
        ):
            with self.subTest(name=name):
                self.assertIsInstance(
                    self.author_client.get(name).context.get('form'),
                    NoteForm
                )
