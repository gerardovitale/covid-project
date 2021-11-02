import unittest

from application import init_app
from application.config.Config import TestingConfig


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = init_app(config=TestingConfig())
        self.client = self.app.test_client()
        self.mongo_db = TestingConfig().DATABASE_OBJ
        # with self.app.app_context():
        #     pass

    def tearDown(self):
        pass
