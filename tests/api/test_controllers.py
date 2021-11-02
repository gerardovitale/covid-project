from tests.api import BaseTestClass


class TestControllers(BaseTestClass):

    def test_home_controller_client(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)

    def test_get_vaccination_summary_json_client(self):
        res = self.client.get('/vaccination_summary/json/italy')
        self.assertEqual(200, res.status_code)
    