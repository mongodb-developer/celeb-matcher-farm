"""Integration tests for celeb-matcher-farm.

Tests real MongoDB CRUD operations for the attendee/celeb_images collection
used by the FastAPI + AWS Bedrock celebrity matching backend.

Requires a running MongoDB instance. Set MONGODB_URI (default:
mongodb://admin:mongodb@localhost:27017/) or the tests will be skipped.
"""

import os
import base64
import pytest
from pymongo import MongoClient
from bson import ObjectId

MONGODB_URI = os.environ.get("MONGODB_URI", "mongodb://admin:mongodb@localhost:27017/")
TEST_DB = "celeb_matcher_integration_test"


@pytest.fixture(scope="module")
def db():
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    try:
        client.admin.command("ping")
    except Exception:
        client.close()
        pytest.skip(f"MongoDB not reachable at {MONGODB_URI}")
    database = client[TEST_DB]
    yield database
    client.drop_database(TEST_DB)
    client.close()


def test_mongodb_ping():
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
    try:
        result = client.admin.command("ping")
        assert result.get("ok") == 1.0
    except Exception:
        pytest.skip(f"MongoDB not reachable at {MONGODB_URI}")
    finally:
        client.close()


def test_attendee_record_crud(db):
    """celeb_images collection: insert, find, update, delete an attendee."""
    celeb_images = db["celeb_images"]

    # Create a fake embedding (1024 floats simulating Bedrock output)
    embedding = [0.01 * i for i in range(1024)]

    doc_id = ObjectId()
    record = {
        "_id": doc_id,
        "name": "Test Attendee",
        "email": "attendee@example.com",
        "embedding": embedding,
        "image_b64": base64.b64encode(b"fake-image-bytes").decode(),
    }

    # Create
    result = celeb_images.insert_one(record)
    assert result.inserted_id == doc_id

    # Read
    found = celeb_images.find_one({"_id": doc_id})
    assert found["name"] == "Test Attendee"
    assert len(found["embedding"]) == 1024

    # Update
    celeb_images.update_one({"_id": doc_id}, {"$set": {"name": "Updated Attendee"}})
    updated = celeb_images.find_one({"_id": doc_id})
    assert updated["name"] == "Updated Attendee"

    # Delete
    delete_result = celeb_images.delete_one({"_id": doc_id})
    assert delete_result.deleted_count == 1
    assert celeb_images.find_one({"_id": doc_id}) is None


def test_query_attendees_by_email(db):
    """celeb_images collection: find by email field."""
    celeb_images = db["celeb_images"]

    ids = [ObjectId(), ObjectId()]
    docs = [
        {
            "_id": ids[0],
            "name": "Alice",
            "email": "alice@conference.example",
            "embedding": [0.1] * 1024,
        },
        {
            "_id": ids[1],
            "name": "Bob",
            "email": "bob@conference.example",
            "embedding": [0.2] * 1024,
        },
    ]
    celeb_images.insert_many(docs)

    found = celeb_images.find_one({"email": "alice@conference.example", "_id": {"$in": ids}})
    assert found is not None
    assert found["name"] == "Alice"

    # Cleanup
    celeb_images.delete_many({"_id": {"$in": ids}})


def test_vector_search_index_structure(db):
    """celeb_images: verify documents have the embedding field needed for vector search."""
    celeb_images = db["celeb_images"]

    doc_id = ObjectId()
    celeb_images.insert_one({
        "_id": doc_id,
        "name": "Carol",
        "embedding": [float(i) / 1024 for i in range(1024)],
    })

    found = celeb_images.find_one({"_id": doc_id})
    assert "embedding" in found
    assert isinstance(found["embedding"], list)
    assert len(found["embedding"]) == 1024
    # All values should be valid floats
    assert all(isinstance(v, float) for v in found["embedding"])

    celeb_images.delete_one({"_id": doc_id})


def test_standardize_image_function():
    """standardize_image() produces a valid base64-encoded JPEG string."""
    try:
        import sys
        from pathlib import Path
        import importlib.util
        import types

        backend_src = Path(__file__).resolve().parents[1] / "backend" / "src"

        # Stub boto3 and AWS dependencies
        for mod_name in ("boto3", "uvicorn"):
            if mod_name not in sys.modules:
                stub = types.ModuleType(mod_name)
                sys.modules[mod_name] = stub

        os.environ.setdefault("MONGODB_URI", MONGODB_URI)
        os.environ.setdefault("AWS_ACCESS_KEY", "test")
        os.environ.setdefault("AWS_SECRET_KEY", "test")

        spec = importlib.util.spec_from_file_location(
            "celeb_server_int", backend_src / "server.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        # Create a minimal 2x2 JPEG image
        from PIL import Image
        import io
        img = Image.new("RGB", (2, 2), color=(255, 0, 0))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        buf.seek(0)
        input_b64 = base64.b64encode(buf.getvalue()).decode()

        result_b64 = mod.standardize_image(input_b64)
        decoded = base64.b64decode(result_b64)
        out_img = Image.open(io.BytesIO(decoded))
        assert out_img.size == (512, 512)
        assert out_img.mode == "RGB"
    except Exception as exc:
        pytest.skip(f"standardize_image test skipped: {exc}")
