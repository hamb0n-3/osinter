from .base import ModuleTestBase


class TestSSLCert(ModuleTestBase):
    targets = ["127.0.0.1:9999", "osintertest.notreal"]
    config_overrides = {"scope": {"report_distance": 1}}

    def check(self, module_test, events):
        assert len(events) == 7
        assert 1 == len(
            [
                e
                for e in events
                if e.data == "www.osintertest.notreal" and str(e.module) == "sslcert" and e.scope_distance == 0
            ]
        ), "Failed to detect subject alternate name (SAN)"
        assert 1 == len(
            [e for e in events if e.data == "test.notreal" and str(e.module) == "sslcert" and e.scope_distance == 1]
        ), "Failed to detect main subject"
