# coding=utf-8

import enum


class DiscountTypes(enum.Enum):
    PERCENTAGE = '%'
    AMOUNT = '$'


class PackageTypes(enum.Enum):
    TIN = 'tin'
    LOAF = 'loaf'
    BAG = 'bag'
    BOTTLE = 'bottle'
