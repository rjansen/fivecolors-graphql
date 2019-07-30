from django.db import models
from django.contrib.postgres import fields as pgfields
import hashlib


def sha1(v):
    if v:
        h = hashlib.sha1()
        h.update(v.encode('utf-8'))
        return h.hexdigest()


class Set(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=15)
    asset = pgfields.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class Rarity():
    COMMON = sha1('Rarity#Common')
    UNCOMMON = sha1('Rarity#Uncommon')
    RARE = sha1('Rarity#Rare')
    MYTHIC_RARE = sha1('Rarity#Mythic Rare')
    SPECIAL = sha1('Rarity#Special')
    LAND = sha1('Rarity#Land')
    PROMO = sha1('Rarity#Promo')
    BONUS = sha1('Rarity#Bonus')

    ALL = [
        (COMMON, 'Common'),
        (UNCOMMON, 'Unccommon'),
        (RARE, 'Rare'),
        (MYTHIC_RARE, 'Mythic Rare'),
        (SPECIAL, 'Special'),
        (LAND, 'Land'),
        (PROMO, 'Promo'),
        (BONUS, 'Bonus'),
    ]


class Card(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    name = models.CharField(max_length=255)
    types = pgfields.ArrayField(models.CharField(max_length=128))
    costs = pgfields.ArrayField(models.CharField(max_length=5), default=list)
    number_cost = models.DecimalField(default=0, max_digits=14, decimal_places=4)
    id_external = models.CharField(max_length=100)
    id_rarity = models.CharField(choices=Rarity.ALL, max_length=40)
    # rarity = models.ForeignKey('Rarity', on_delete=models.PROTECT)
    # id_set = models.CharField(max_length=40)
    set = models.ForeignKey('Set', on_delete=models.PROTECT, db_column='id_set', max_length=40)
    id_asset = models.CharField(max_length=40)
    rate = models.DecimalField(default=0, max_digits=14, decimal_places=4)
    rate_votes = models.DecimalField(default=0, max_digits=10, decimal_places=0)
    rules = pgfields.ArrayField(models.CharField(max_length=512), default=list)
    order_external = models.CharField(null=True, max_length=15)
    artist = models.CharField(null=True, max_length=255)
    flavor = models.TextField(null=True, max_length=1024)
    data = pgfields.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name
