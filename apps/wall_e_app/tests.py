from django.test import TestCase, Client
import bcrypt
from .models import *
from .views import *

class Wall_ETest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(id=1, first_name = "FooBar", last_name = "BarFoo", email = "fbbf@test.com", password = "12345678_Test")
        test_message = Message.objects.create(id=1, message = "To FooBar or not to FooBar, that is this Message-Model's unit test question", user= test_user)
        test_comment_message = Message.objects.create(id=2, message = "This Message is for the Comment-Model test", user= test_user)
        test_comment = Comment.objects.create(id=1, Comment= "Comment-Model Unit Test", user= test_user, message = test_comment_message)

    def test_index_url(self):
        c = Client()
        idx_response = c.get('/')
        self.assertEqual(idx_response.status_code, 200)

    def test_usermodel_create(self):
        u = User.objects.create(first_name = "John", last_name = "Doe", email = "jd@test.com", password = "12345678_Doe")
        self.assertEqual(u.first_name, "John")
        self.assertEqual(u.last_name, "Doe")
        self.assertEqual(u.email, "jd@test.com")
        self.assertEqual(u.password, "12345678_Doe")

    def test_usermodel_get(self):
        u = User.objects.get(id =1)
        self.assertEqual(u.id, 1)
        self.assertIsInstance(u, User)

    def test_usermodel_edit(self):
        u = User.objects.first()
        u.first_name = "EDITED_FooBar"
        u.last_name = "EDITED_BarFoo"
        u.email = "fbbf_editusermodel_test@test.com"
        u.password = "Test12345678"
        u.save()
        edited_u = User.objects.first()
        self.assertEqual(edited_u.first_name, "EDITED_FooBar")
        self.assertEqual(edited_u.last_name, "EDITED_BarFoo")
        self.assertEqual(edited_u.email, "fbbf_editusermodel_test@test.com")
        self.assertEqual(edited_u.password, "Test12345678")

    def test_messagemodel_create(self):
        m = Message.objects.create(message = "Mr. BarFoo's Message-Model Unit Test!", user=User.objects.get(id=1))
        self.assertEqual(m.message, "Mr. BarFoo's Message-Model Unit Test!")
        self.assertEqual(m.user, User.objects.get(id=1))

    def test_messagemodel_get(self):
        m = Message.objects.get(id=1)
        self.assertEqual(m.id, 1)
        self.assertIsInstance(m, Message)

    def test_messagemodel_edit(self):
        m = Message.objects.first()
        m.message = "EDITED_To FooBar or not to FooBar, that is this unit test's question"
        m.save()
        edited_m = Message.objects.first()
        self.assertEqual(edited_m.message, "EDITED_To FooBar or not to FooBar, that is this unit test's question")

    def test_messagemodel_delete(self):
        m_deleted = Message.objects.get(id=1).delete()[0]
        self.assertEqual(m_deleted, 1)

    def test_commentmodel_create(self):
        cmt = Comment.objects.create(Comment = "Does anyone think differently on FooBar, wonders this comment model unit test?!", user= User.objects.get(id=1), message= Message.objects.get(id=2))
        self.assertEqual(cmt.Comment, "Does anyone think differently on FooBar, wonders this comment model unit test?!")
        self.assertEqual(cmt.user, User.objects.get(id=1))
        self.assertEqual(cmt.message, Message.objects.get(id=2))

    def test_commentmodel_get(self):
        cmt = Comment.objects.get(id=1)
        self.assertEqual(cmt.id, 1)
        self.assertIsInstance(cmt, Comment)

    def test_commentmodel_edit(self):
        cmt = Comment.objects.first()
        cmt.Comment = "EDITED_Comment Model Unit Test"
        cmt.save()
        edited_cmt = Comment.objects.first()
        self.assertEqual(edited_cmt.Comment, "EDITED_Comment Model Unit Test")

    def test_commentmodel_delete(self):
        cmt_deleted = Comment.objects.get(id=1).delete()[0]
        self.assertEqual(cmt_deleted, 1)

    def test_view_register(self):
        c = Client()
        postData = {
            "first_name": "Gordon_Test",
            "last_name" : "Allen_Test",
            "email": "g_test@test.com",
            "password": "12345678_Test",
            "confirm_password": "12345678_Test"
        }
        register_response = c.post('/register', postData)
        self.assertEqual(register_response.status_code, 302)
        newly_created_user = User.objects.last()
        self.assertEqual(newly_created_user.first_name, postData['first_name'])
        self.assertEqual(newly_created_user.last_name, postData['last_name'])
        self.assertEqual(newly_created_user.email, postData['email'])
        self.assertTrue(bcrypt.checkpw(postData['password'].encode('utf8'), newly_created_user.password.encode('utf8')))
