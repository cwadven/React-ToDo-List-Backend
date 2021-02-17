from django.db import models
from django.contrib.auth.models import AbstractUser


from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

class Profile(AbstractUser):
    # 추가적인 속성

    def __str__(self):
        return '%s' % (self.username)

    # 만약 이미지 추가 - 이미지 메타 데이터 회전
    # 저장할때 이미지는 orientation 맞춰서 저장 또한 전부 삭제 exif정보
    # def save(self, *args, **kwargs): 
    #     if self.이미지속성:
    #         pilImage = Img.open(BytesIO(self.이미지속성.read()))
    #         try:
    #             for orientation in ExifTags.TAGS.keys():
    #                 if ExifTags.TAGS[orientation] == 'Orientation':
    #                     break
    #             exif = dict(pilImage._getexif().items())

    #             if exif[orientation] == 3:
    #                 pilImage = pilImage.rotate(180, expand=True)
    #             elif exif[orientation] == 6:
    #                 pilImage = pilImage.rotate(270, expand=True)
    #             elif exif[orientation] == 8:
    #                 pilImage = pilImage.rotate(90, expand=True)

    #             output = BytesIO()
    #             pilImage.save(output, format='JPEG', quality=100)
    #             output.seek(0)
    #             self.이미지속성 = File(output, self.이미지속성.name)
    #         except:
    #             pass

    #     return super(Profile, self).save(*args, **kwargs)