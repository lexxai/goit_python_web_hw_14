import sys
import os
import unittest
from unittest.mock import MagicMock
from pathlib import Path

from sqlalchemy.orm import Session

hw_path: str = str(Path(__file__).resolve().parent.parent.joinpath("hw14"))
sys.path.append(hw_path)
# print(f"{hw_path=}", sys.path)
os.environ["PYTHONPATH"] += os.pathsep + hw_path
# print(f'{os.environ["PYTHONPATH"]=}')


from hw14.src.database.models import User, Contact
from hw14.src.shemas.contact import ContactModel, ContactFavoriteModel, ContactResponse
from hw14.src.shemas.users import UserModel, UserResponse, UserDetailResponse, NewUserResponse

from hw14.src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    create,
    update,
    delete,
    favorite_update,
    search_birthday,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        favorite = True
        q = self.session.query().filter_by()
        if favorite is not None:
            q = q.filter_by()
        q.offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user_id=self.user.id, favorite=favorite, db=self.session)  # type: ignore
        self.assertEqual(result, contacts)

    async def test_get_contact_found_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)

    async def test_get_contact_found_by_email(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_email(email="as@ee.ua", user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)

    async def test_get_contact_not_found_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = None
        result = await get_contact_by_id(contact_id=1, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)

    async def test_get_contact_not_found_by_email(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = None
        result = await get_contact_by_email(email="as@ee.ua", user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)


    async def test_create_contact(self):
        body = ContactModel(first_name="test1", last_name="test2", email="aa@uu.uu",phone="+380 (44) 1234567")
        result = await create(body=body, user_id=self.user.id, db=self.session) # type: ignore
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertTrue(hasattr(result, "id"))


# class TestNotes(unittest.IsolatedAsyncioTestCase):

#     def setUp(self):
#         self.session = MagicMock(spec=Session)
#         self.user = User(id=1)

#     async def test_get_notes(self):
#         notes = [Note(), Note(), Note()]
#         self.session.query().filter().offset().limit().all.return_value = notes
#         result = await get_notes(skip=0, limit=10, user=self.user, db=self.session)
#         self.assertEqual(result, notes)

#     async def test_get_note_found(self):
#         note = Note()
#         self.session.query().filter().first.return_value = note
#         result = await get_note(note_id=1, user=self.user, db=self.session)
#         self.assertEqual(result, note)

#     async def test_get_note_not_found(self):
#         self.session.query().filter().first.return_value = None
#         result = await get_note(note_id=1, user=self.user, db=self.session)
#         self.assertIsNone(result)

#     async def test_create_note(self):
#         body = NoteModel(title="test", description="test note", tags=[1, 2])
#         tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
#         self.session.query().filter().all.return_value = tags
#         result = await create_note(body=body, user=self.user, db=self.session)
#         self.assertEqual(result.title, body.title)
#         self.assertEqual(result.description, body.description)
#         self.assertEqual(result.tags, tags)
#         self.assertTrue(hasattr(result, "id"))

#     async def test_remove_note_found(self):
#         note = Note()
#         self.session.query().filter().first.return_value = note
#         result = await remove_note(note_id=1, user=self.user, db=self.session)
#         self.assertEqual(result, note)

#     async def test_remove_note_not_found(self):
#         self.session.query().filter().first.return_value = None
#         result = await remove_note(note_id=1, user=self.user, db=self.session)
#         self.assertIsNone(result)

#     async def test_update_note_found(self):
#         body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
#         tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
#         note = Note(tags=tags)
#         self.session.query().filter().first.return_value = note
#         self.session.query().filter().all.return_value = tags
#         self.session.commit.return_value = None
#         result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
#         self.assertEqual(result, note)

#     async def test_update_note_not_found(self):
#         body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
#         self.session.query().filter().first.return_value = None
#         self.session.commit.return_value = None
#         result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
#         self.assertIsNone(result)

#     async def test_update_status_note_found(self):
#         body = NoteStatusUpdate(done=True)
#         note = Note()
#         self.session.query().filter().first.return_value = note
#         self.session.commit.return_value = None
#         result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
#         self.assertEqual(result, note)

#     async def test_update_status_note_not_found(self):
#         body = NoteStatusUpdate(done=True)
#         self.session.query().filter().first.return_value = None
#         self.session.commit.return_value = None
#         result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
#         self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
