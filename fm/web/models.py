from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

class Administrator(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    class Meta:
        db_table = 'administrator'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        slug = slugify(self.name)
        return reverse('mutual_funds_by_administrator', kwargs={'administrator_id': self.id, 'slug': slug})

class MutualFund(models.Model):
    administrator = models.ForeignKey(Administrator)
    run = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'mutual_fund'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        slug = slugify(self.name)
        return reverse('mutual_fund_detail', kwargs={'mutual_fund_id': self.id, 'slug': slug})

    def get_last_day(self):
        return self.day_set.all()[0]

    def get_line_data(self):
        response = '{"cols":[{"id":"date","label":"Fecha","type":"date"},{"id":"nav","label":"Valor Cuota","type":"number"}],"rows":['
        rows = []
        days = self.day_set.values('date', 'nav').all()
        for day in days:
            rows.append('{"c":[{"v":"%s"},{"v":%s}]}' % (day['date'], day['nav']))
        response += ','.join(rows)
        response += ']}'
        return response

class Day(models.Model):
    date = models.DateField()
    mutual_fund = models.ForeignKey(MutualFund)
    nav = models.FloatField()
    daily_nominal = models.FloatField()
    nominal_30_days = models.FloatField()
    real_30_days = models.FloatField()
    nominal_3_months = models.FloatField()
    real_3_months = models.FloatField()
    nominal_12_months = models.FloatField()
    real_12_months = models.FloatField()

    class Meta:
        db_table = 'day'
        ordering = ['-date']
        unique_together = ('date', 'mutual_fund')
