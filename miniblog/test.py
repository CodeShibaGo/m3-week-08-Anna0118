import unittest
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

from app.models import User
from app import app, db

# print(os.getenv('DATABASE_URL')) #De-bug路徑
os.environ['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')


class UserModelCase(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        db.session.execute(text('DELETE FROM followers'))
        db.session.query(User).delete()
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        # db.session.execute(text('DELETE FROM followers'))
        # db.session.query(User).delete()
        self.app_context.pop()

    def test_follow(self):
        u1 = User(username='susan', email='susan@example.com')
        u2 = User(username='john', email='john@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.following.all(), [])
        self.assertEqual(u2.followers.all(), [])

        # u1追蹤u2
        u1.follow(u2)
        db.session.commit()

        # u1是否追蹤u2
        self.assertTrue(u1.is_following(u2))

        # u1的追蹤人數
        self.assertEqual(u1.following.count(), 1)
        # u2的追蹤者人數
        self.assertEqual(u2.followers.count(), 1)

        # u1追蹤的人是不是u2
        self.assertEqual(u1.following.all()[0].id, u2.id)
        # u2的追蹤者是不是u1
        self.assertEqual(u2.followers.all()[0].id, u1.id)

        # 退追蹤
        u1.unfollow(u2)
        db.session.commit()

        # 再次驗證
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following.count(), 0)
        self.assertEqual(u2.followers.count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
