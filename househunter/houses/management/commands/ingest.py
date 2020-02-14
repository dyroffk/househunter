import csv
import datetime
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from houses.models import House

class Command(BaseCommand):
    help = 'Ingest housing data from CSV'

    DATE_FIELDS = ('last_sold_date', 'rentzestimate_last_updated', 'zestimate_last_updated')
    NULLABLES = ('bathrooms', 'home_size', 'last_sold_date', 'last_sold_price', 'property_size', 'rent_price',
                 'rentzestimate_amount', 'rentzestimate_last_updated', 'year_built', 'zestimate_amount')

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def parse_price(self, price):
        assert price[0] == '$'
        multiplier = price[-1]
        base_price = Decimal(price[1:-1])

        if multiplier == 'K':
            return int(base_price * 1_000)
        if multiplier == 'M':
            return int(base_price * 1_000_000)
        raise RuntimeError('Unknown price multiplier: "%s"' % multiplier)

    def handle(self, *args, **options):
        filepath = options['filepath']
        self.stdout.write('Ingesting Houses from "%s"' % filepath)

        with open(filepath) as fp:
            reader = csv.DictReader(fp)
            error_rows = []
            created_count = 0
            for row in reader:
                # self.stdout.write('House: %s' % row)

                # TODO: Need to convert area if other units encountered
                assert(row['area_unit'] == 'SqFt')
                del row['area_unit']

                for nullable in self.NULLABLES:
                   if row[nullable] == '':
                       row[nullable] = None

                row['listing_link'] = row['link']
                del row['link']

                row['listing_price'] = self.parse_price(row['price'])
                del(row['price'])

                for field in self.DATE_FIELDS:
                    row[field] = None if row[field] in ('', None) else datetime.datetime.strptime(row[field], '%m/%d/%Y')

                try:
                    _, created = House.objects.get_or_create(**row)
                    if created == True:
                        created_count += 1
                except IntegrityError as e:
                    self.stdout.write("Error inserting row: {} -- {}".format(e, row))
                    error_rows.append((row, e))

        self.stdout.write("Finished ingesting House data")
        self.stdout.write("Successfully created {} Houses".format(created_count))
        self.stdout.write("Errored on {} rows".format(len(error_rows)))
