from django.db import models
from datetime import date

class ModelFile(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='documents/')
    result = models.IntegerField(blank=True, null=True)
    proba = models.FloatField(default=0.0)
    registered_date = models.DateField(default=date.today())

    #管理画面に表示方法を定義：必須項目が入っているかどうかで表示内容を分ける
    def __str__(self):
        if self.proba == 0.0:
            return '%d,%s,%s' % (self.id, self.image, self.registered_date.strftime('%Y-%m-%d'))
        else:
            return '%d,%s,%s,%s' % (self.id, self.image, self.registered_date.strftime('%Y-%m-%d'),self.result)