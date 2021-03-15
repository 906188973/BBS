from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """用户"""
    POWER_CHOICES = (
        (1, "普通用户"),
        (2, "版务"),
        (3, "版主"),
        (4, "管理员"),
    )
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)
    email = models.EmailField(verbose_name='邮件', max_length=32)
    mobile_phone = models.CharField(verbose_name='手机号', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    head_portrait = models.ImageField(verbose_name='头像', null=True, upload_to='headPortrait/')
    power = models.SmallIntegerField(choices=POWER_CHOICES, default=1)
    power_name = models.CharField(max_length=20, default='普通用户')
    describe = models.TextField(verbose_name='个性签名', null=True)

    def __str__(self):
        return self.username

class Forum(models.Model):
    """版块"""
    forum_name = models.CharField(verbose_name='版块名', max_length=32, db_index=True)
    topic_count = models.IntegerField(default=0)
    concern_count = models.IntegerField(default=0)
    date_added = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    moderator = models.ForeignKey(UserInfo, null=True, on_delete=models.SET_NULL)
    picture = models.ImageField(verbose_name='图片', null=True, upload_to='picture/')

    def __str__(self):
        return self.forum_name

class Topic(models.Model):
    """帖子主题"""
    topic_text = models.CharField(max_length=200)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    floor_count = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic_text

class Floor(models.Model):
    """楼层"""
    floor_text = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    floor_number = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.floor_text[:50] + '...'

class Comment(models.Model):
    """帖子回复"""
    text = models.TextField(max_length=200)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    owner = models.ForeignKey(UserInfo, related_name="comments", on_delete=models.DO_NOTHING)
    by_owner = models.ForeignKey(UserInfo, null=True, related_name="replies", on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50] + '...'

class UserToForum(models.Model):
    """用户关注模块表"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class Collect(models.Model):
    """用户收藏帖子表"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

class ForumPower(models.Model):
    """版块权限表"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    forum = models.ForeignKey(Forum, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)