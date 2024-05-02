import sys
from PIL import Image
import base64
import os
import io
import boto3
import json
import uvicorn

from contextlib import asynccontextmanager

from pymongo import MongoClient

# from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI

MONGODB_URI = os.environ["MONGODB_URI"]
AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]

class Bedrock:
    def __init__(self, aws_access_key, aws_secret_key, region="us-east-1"):
        self._runtime = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region,
        )

    @staticmethod
    def construct_body(base64_string, text=None):
        """Construct the request body for Bedrock"""
        if text:
            return json.dumps(
                {
                    "inputImage": base64_string,
                    "embeddingConfig": {"outputEmbeddingLength": 1024},
                    "inputText": text,
                }
            )
        return json.dumps(
            {
                "inputImage": base64_string,
                "embeddingConfig": {"outputEmbeddingLength": 1024},
            }
        )

    def get_embedding(self, body):
        """Get the embedding from Bedrock's titan_multimodal model."""
        response = self._runtime.invoke_model(
            body=body,
            modelId="amazon.titan-embed-image-v1",
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        return response_body["embedding"]


def generate_image_description(self, images_base64_strs, image_base64):
    """
    Generate image description using Claude 3 Sonnet
    """
    claude_body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "system": "Please act as face comperison analyzer.",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": images_base64_strs[0],
                            },
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": images_base64_strs[1],
                            },
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": images_base64_strs[2],
                            },
                        },
                        {
                            "type": "text",
                            "text": "Please let the user know how his first image is similar to the other 3 and which one is the most similar?",
                        },
                    ],
                }
            ],
        }
    )

    claude_response = self._runtime.invoke_model(
        body=claude_body,
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        accept="application/json",
        contentType="application/json",
    )
    response_body = json.loads(claude_response.get("body").read())
    # Assuming the response contains a field 'content' with the description
    return response_body["content"][0].get("text", "No description available")


@asynccontextmanager
async def lifecycle(app: FastAPI):
    app.client = client = MongoClient(MONGODB_URI)
    app.db = database = client.get_default_database()
    # db_name = "celebrity_1000_embeddings"
    collection_name = "celeb_images"
    app.celeb_images = database.get_collection(collection_name)

    pong = database.command("ping")
    if int(pong["ok"]) != 1:
        raise Exception("Cluster connection is not okay!")

    # AWS Bedrock client setup
    app.bedrock = Bedrock(AWS_ACCESS_KEY, AWS_SECRET_KEY)

    yield

    app.client.close()


app = FastAPI(lifecycle=lifecycle, debug=True)


# # Main function to start image search
# @app.post("/search")
# def start_image_search(image: Image, text: str | None):
#     if not image:
#         raise Exception(
#             "Please upload an image first, make sure to press the 'Submit' button after selecting the image."
#         )
#     buffered = io.BytesIO()
#     image = image.resize((800, 600))
#     image.save(buffered, format="JPEG", quality=85)
#     img_byte = buffered.getvalue()
#     img_base64 = base64.b64encode(img_byte)
#     img_base64_str = img_base64.decode("utf-8")
#     body = app.bedrock.construct_bedrock_body(img_base64_str, text)
#     embedding = app.bedrock.get_embedding(body)

#     doc = list(
#         app.celeb_images.aggregate(
#             [
#                 {
#                     "$vectorSearch": {
#                         "index": "vector_index",
#                         "path": "embeddings",
#                         "queryVector": embedding,
#                         "numCandidates": 15,
#                         "limit": 3,
#                     }
#                 },
#                 {"$project": {"image": 1}},
#             ]
#         )
#     )

#     images = []
#     images_base64_strs = []
#     for image_doc in doc:
#         pil_image = Image.open(io.BytesIO(base64.b64decode(image_doc["image"])))
#         img_byte = io.BytesIO()
#         pil_image.save(img_byte, format="JPEG")
#         img_base64 = base64.b64encode(img_byte.getvalue()).decode("utf-8")
#         images_base64_strs.append(img_base64)
#         images.append(pil_image)

#     description = app.bedrock.generate_image_description(
#         images_base64_strs, img_base64_str
#     )
#     return images, description


@app.get("/api")
async def index():
    return "hello"


def main(argv=sys.argv[1:]):
    uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=True)


if __name__ == "__main__":
    main()
