from flask_testing import TestCase

from app import create_app, db


class BaseServiceTest(TestCase):
    ENV = 'test'

    def create_app(self):
        return create_app(env=self.ENV)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _add_to_db(self, record):
        db.session.add(record)
        db.session.commit()
        self.assertTrue(record in db.session)
        return record
