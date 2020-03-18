from django.db import models


class BaseModel(models.Model):
    """抽象基类"""
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("修改时间", auto_now=True)
    is_delete = models.BooleanField('是否删除',default=False)

    class Meta:
        # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表
        abstract = True