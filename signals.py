import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from home.models import UserPhoto

@receiver(post_save, sender=UserPhoto)
def resize_and_rename_profile_photo(sender, instance, **kwargs):
    if instance.photo:
        try:
            old_path = instance.photo.path
            ext = os.path.splitext(old_path)[1]
            new_filename = f"{instance.user.username}.jpg"
            new_path = os.path.join(os.path.dirname(old_path), new_filename)

            if old_path != new_path:
                if os.path.exists(new_path):
                    os.remove(new_path)
                os.rename(old_path, new_path)
                instance.photo.name = os.path.join(os.path.dirname(instance.photo.name), new_filename)
                instance.save(update_fields=['photo'])

            img = Image.open(new_path)
            img = img.convert("RGB")
            img = img.resize((400, 400), Image.Resampling.LANCZOS)
            img.save(new_path, format="JPEG", quality=75, optimize=True)

        except Exception as e:
            print("Error resizing or renaming image:", e)
