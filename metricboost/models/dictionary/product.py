from tortoise import fields

from metricboost.models.base import BaseModel, TimestampMixin


class Product(BaseModel, TimestampMixin):
    """产品字典信息"""

    id = fields.IntField(primary_key=True)
    vin = fields.CharField(max_length=20, unique=True, description="识别号")

    class Meta:
        table = "product"
        table_description = "产品信息"
