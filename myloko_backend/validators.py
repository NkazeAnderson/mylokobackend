from os.path import splitext
from rest_framework import serializers

def validateMedia(media, type: str):
    name, extension = splitext(media.name)
    extension = extension.lower()
    content_type = media.content_type
    if type == "video":
        if content_type != "video/mp4" and extension != ".mp4":
            raise serializers.ValidationError({"video": "Not mp4"}, code=400)
        return
    else:
        if ((content_type != "image/png" and extension != ".png")):
            if ((content_type != "image/jpeg" and (extension != ".jpg" or extension != ".jpeg"))):
                raise serializers.ValidationError({"image": "Not png/jpeg"}, code=400)
        return
