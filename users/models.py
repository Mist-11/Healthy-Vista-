from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    identity = models.CharField(max_length=10, default="用户")
    timestamp = models.DateTimeField()
    sex = models.CharField(max_length=1, choices=(('M', '男'), ('F', '女')), blank=True, null=True)


class SimpleRecord(models.Model):
    name = models.CharField(max_length=128)
    record_type = models.CharField(max_length=128)
    timestamp = models.BigIntegerField()
    file_path = models.CharField(max_length=256)  # 用于存储PDF文件路径

    @classmethod
    def pre_record(cls, name, record_type, time, path):
        cls.objects.create(
            name=name,
            record_type=record_type,
            timestamp=time,
            file_path=path
        )


# 邮箱验证
class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name="验证码类型", max_length=10,
                                 choices=(("register", "注册"), ("forget", "找回密码")))
    send_time = models.DateTimeField(verbose_name="发送时间")
