from functools import wraps
from app import create_app


def with_context(test):
    @wraps(test)
    def _wrapped_test(self):
        with self.app.app_context():
            with self.app.test_request_context():
                test(self)
    return _wrapped_test


def with_client(test):
    @wraps(test)
    def _wrapped_test(self):
        with self.app.test_client() as client:
            test(self, client)
    return _wrapped_test


def setUpApp(self):
    self.app = create_app()
    self.app.config.from_object('config.TestingConfig')