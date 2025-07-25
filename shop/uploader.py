from io import BytesIO
import os

from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage


load_dotenv()


storage_bucket_cert = {
    "type": "service_account",
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fm6th%40inventory-d3e2b.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}


cred = credentials.Certificate(storage_bucket_cert)
firebase_admin.initialize_app(
    cred, {"storageBucket": os.getenv("FIREBASE_BUCKET")})


def upload_image(images):
    urls = []
    try:
        bucket = storage.bucket()
        for image in images:
            content = image.file.read()
            blob = bucket.blob(image.name)
            file_obj = BytesIO(content)
            blob.upload_from_file(file_obj, content_type=image.content_type)

            blob.make_public()
            url = blob.public_url
            urls.append(url)
    except Exception as e:
        print(f"Error uploading image: {e}")
        return False
    return urls
