from fm.web.models import *
from django.conf import settings
from django.core.management.base import BaseCommand
from junar_api import junar_api
import datetime

class Command(BaseCommand):
    args = '<administrator_code, year, month, day>'
    help = 'Download the data using Junar.com, from aafm.cl for a specific administrator and date'

    def handle(self, *args, **options):
        administrator_code = args[0]
        year = args[1]
        month = args[2]
        day = args[3]

        administrator = Administrator.objects.get(code=administrator_code)
        self.stdout.write("getting %s-%s-%s for %s" % (year, month, day, administrator))
        junar_api_client = junar_api.Junar(settings.JUNAR_AUTH_KEY, base_uri = 'http://api.junar.com')
        datastream = junar_api_client.datastream('FONDO-MUTUO-DESDE-AAFM')
        params = [administrator_code, day, month, year]
        response = datastream.invoke(params = params, output = 'json_array')
        result = response['result']
        for row in result[2:-4]:
            run = row[1]
            mutual_fund_name = row[2]
            date = datetime.datetime(int(year), int(month), int(day))
            theday = Day()
            theday.date = date
            theday.nav = clean(row[3])
            theday.daily_nominal = clean(row[4])
            theday.nominal_30_days = clean(row[5])
            theday.real_30_days = clean(row[6])
            theday.nominal_3_months = clean(row[7])
            theday.real_3_months = clean(row[8])
            theday.nominal_12_months = clean(row[9])
            theday.real_12_months = clean(row[10])
            mutual_fund, is_new = MutualFund.objects.get_or_create(name=mutual_fund_name
                                                , administrator=administrator
                                                , defaults = {'run': run})
            theday.mutual_fund = mutual_fund
            theday.save()

def clean(s):
    if s != '-':
        return float(s.replace(' %', '').replace('.', '').replace(',', '.'))
    else:
        return 0
