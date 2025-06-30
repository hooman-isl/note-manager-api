from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from note.models import NoteFile
from note.utils import safe_remove_file


@receiver(pre_save, sender=NoteFile)
def cleanup_old_file_on_update(sender, instance, **kwargs):
    if instance.pk is None:
        return None

    old_file = NoteFile.objects.get(pk=instance.pk).file
    safe_remove_file(old_file)


@receiver(post_delete, sender=NoteFile)
def delete_file_on_instance_delete(sender, instance, **kwargs):
    safe_remove_file(instance.file)