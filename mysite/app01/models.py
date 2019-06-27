from django.db import models

class user(models.Model):   # 定义一个类，对应一个表，必须继承models
    name = models.CharField(max_length=32)   # 定义varchar类型，并指定长度
    pwd = models.CharField(max_length=32)


# class Book(models.Model):
#     title = models.CharField(max_length=32)
#     price = models.DecimalField(max_digits=6,decimal_places=2)
#     create_time = models.DateField()

class Project(models.Model):
    id = models.AutoField(primary_key=True) # 主键
    name = models.CharField(max_length=32)


# class Author(models.Model):
#     name = models.CharField(max_length=32)


class Hostlist(models.Model):
    hostname = models.CharField(max_length=32)
    ip_addr = models.GenericIPAddressField()
    project = models.ForeignKey('Project',on_delete=models.CASCADE)

