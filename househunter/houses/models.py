from django.db import models


class House(models.Model):
    APARTMENT = 'AP'
    CONDO = 'CO'
    DUPLEX = 'DX'
    MISC = 'MX'
    MULTI_2TO4 = 'MF'
    SINGLE_FAMILY = 'SF'
    VACANT_RESIDENTIAL = 'VR'
    HOME_TYPE_CHOICES = (
        (APARTMENT, 'Apartment'),
        (CONDO, 'Condominium'),
        (DUPLEX, 'Duplex'),
        (MISC, 'Miscellaneous'),
        (MULTI_2TO4, 'MultiFamily2To4'),
        (SINGLE_FAMILY, 'SingleFamily'),
        (VACANT_RESIDENTIAL, 'VacantResidentialLand'),
    )

    # TODO: Would've expected zillow_id to be unique, but input data has some duplicates
    #  Is the input data bad, or should we relax this constraint?
    zillow_id = models.IntegerField(unique=True)
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    bedrooms = models.IntegerField()
    home_size = models.IntegerField(blank=True, null=True) # In SqFt
    home_type = models.CharField(max_length=2, choices=HOME_TYPE_CHOICES)
    property_size = models.IntegerField(blank=True, null=True) # In SqFt
    year_built = models.IntegerField(blank=True, null=True)

    # May want to keep sale prices in separate model to track over time
    last_sold_date = models.DateField(blank=True, null=True)
    last_sold_price = models.IntegerField(blank=True, null=True)

    # Separate listing model may make sense if tracking listings on multiple platforms
    listing_price = models.IntegerField()
    listing_link = models.URLField()

    # TODO: rent_price in input always empty -- Is there a purpose to keeping this field?
    rent_price = models.IntegerField(blank=True, null=True)

    # May want to consider separate models to track [tax/zestimate/rentzestimate]_value over time
    #  rather than attached directly to House model
    rentzestimate_amount = models.IntegerField(blank=True, null=True)
    rentzestimate_last_updated = models.DateField(blank=True, null=True)
    tax_value = models.IntegerField()
    tax_year = models.IntegerField()
    zestimate_amount = models.IntegerField(blank=True, null=True)
    # TODO: Some zestimate timestamps appear invalid (e.g. 01/01/1970) with no value
    #  Should we bother recording those?
    #  Does some consumer require this field to be populated?
    zestimate_last_updated = models.DateField()

    # Might want to pull out the following address attributes to a separate model
    # and/or generalize for non-US addresses
    # Is there a need to parse out street # from address?
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
