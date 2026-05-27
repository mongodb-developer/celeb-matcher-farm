import base64
import importlib.util
import io
import os
import sys
import types
import unittest
from pathlib import Path

from PIL import Image


class RuntimeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("MONGODB_URI", "mongodb://example/test")
        os.environ.setdefault("AWS_ACCESS_KEY", "x")
        os.environ.setdefault("AWS_SECRET_KEY", "y")

        if "boto3" not in sys.modules:
            boto3 = types.ModuleType("boto3")
            boto3.client = lambda *args, **kwargs: object()
            sys.modules["boto3"] = boto3

        target = Path(__file__).resolve().parents[1] / "backend" / "src" / "server.py"
        spec = importlib.util.spec_from_file_location("celeb_server", target)
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def test_standardize_image_and_payload(self):
        img = Image.new("RGB", (2, 2), color=(255, 0, 0))
        buff = io.BytesIO()
        img.save(buff, format="JPEG")
        b64 = base64.b64encode(buff.getvalue()).decode("utf-8")

        out = self.mod.standardize_image(b64)
        self.assertIsInstance(out, str)
        decoded = base64.b64decode(out)
        self.assertGreater(len(decoded), 0)

        payload = self.mod.SearchPayload(img="data:image/jpeg;base64," + b64, compareWithOtherAttendees=False)
        self.assertFalse(payload.compareWithOtherAttendees)


if __name__ == "__main__":
    unittest.main()
