from .conftest import Base
from notes.forms import NoteForm


class TestContent(Base):
    def test_notes_list_for_author(self):
        object_list = self.author_client.get(
            self.NOTES_LIST_URL
        ).context['object_list']
        self.assertIn(
            self.note,
            object_list
        )
        for note in object_list:
            self.assertEqual(self.note.title, note.title)
            self.assertEqual(self.note.text, note.text)
            self.assertEqual(self.note.slug, note.slug)
            self.assertEqual(self.note.author, note.author)

    def test_notes_list_for_not_author(self):
        self.assertNotIn(
            self.note,
            self.other_author_client.get(
                self.NOTES_LIST_URL
            ).context['object_list']
        )

    def test_authorized_client_has_form(self):
        for name in (
            self.NOTES_ADD_URL,
            self.NOTES_EDIT_URL
        ):
            with self.subTest(name=name):
                self.assertIsInstance(
                    self.author_client.get(name).context.get('form'),
                    NoteForm
                )
