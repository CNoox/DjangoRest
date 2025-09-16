from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from home.models import UserPhoto

@receiver(post_save, sender=UserPhoto)
def resize_profile_photo(sender, instance, **kwargs):
    if instance.photo:
        try:
            img = Image.open(instance.photo.path)

            img = img.convert("RGB")
            img = img.resize((400, 400), Image.Resampling.LANCZOS)

            img.save(instance.photo.path, format="JPEG", quality=75, optimize=True)

        except Exception as e:
            print("Error resizing image:", e)
