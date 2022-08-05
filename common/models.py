from django.db import models

# Create your models here.
class Customer(models.Model):
    # 客户名称
    name = models.CharField(max_length=200)

    # 联系电话
    phonenumber = models.CharField(max_length=200)

    # 地址
    address = models.CharField(max_length=200)

class Medicine(models.Model):
    # 药品名
    name = models.CharField(max_length=200)
    # 药品编号
    sn = models.CharField(max_length=200)
    # 描述
    desc = models.CharField(max_length=200)

import datetime
class Order(models.Model):
    '''
    一个订单肯定是属于一个客户的，而一个客户可以多个订单，即一对多；
    '''
    # 订单名
    name = models.CharField(max_length=200,null=True,blank=True)

    # 创建日期
    create_date = models.DateTimeField(default=datetime.datetime.now)

    # 客户
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    # 订单购买的药品，和Medicine表是多对多 的关系
    #一个订单的药信息肯定是多个，同时一种药也可以对应多个订单，所以多对多
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    # 订单中药品的数量
    amount = models.PositiveIntegerField()
