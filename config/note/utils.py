import os
import uuid
from django.utils import timezone


def generate_upload_path(instance, file_name):
    """
    Return a unique, organized upload path: "<app>/<model>/<YYYY‑MM>/<uuid>.<ext>".
    """
    _, file_extension = os.path.splitext(file_name)
    unique_file_name = f"{uuid.uuid4().hex}{file_extension.lower()}"
    current_month = timezone.now().strftime("%Y-%m")
    return os.path.join(
        f"{instance._meta.app_label}/{instance._meta.model_name}", current_month, unique_file_name
    )


def safe_remove_file(file):
    """
    Safely deletes a file from disk if it exists, ensuring it is closed beforehand.
    """
    if file:
        path = file.path

        if os.path.isfile(path):
            if not file.closed:
                file.close()

            os.remove(path)
            # Set logging (Info), in the future.
            return True

    return False
