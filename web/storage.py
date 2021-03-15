# 给上传的图片重命名
from django.core.files.storage import FileSystemStorage
import os
from django.http import HttpResponse


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, username, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)
        self.username = username

    # 重写 _save方法
    def _save(self, name, content):
        # name为上传文件名称

        # 文件扩展名
        ext = os.path.splitext(name)[1]
        # 文件目录
        d = os.path.dirname(name)
        # 定义文件名，年月日时分秒随机数
        fn = self.username
        # 重写合成文件名
        name = os.path.join(d, fn + ext)
        # 调用父类方法
        return super(ImageStorage, self)._save(name, content)

