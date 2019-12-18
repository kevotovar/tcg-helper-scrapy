# -*- coding: utf-8 -*-
import scrapy


class MylItem(scrapy.Item):
    id = scrapy.Field()
    edid = scrapy.Field()
    slug = scrapy.Field()
    edition_id = scrapy.Field()
    name = scrapy.Field()
    flavour = scrapy.Field()
    ability = scrapy.Field()
    ability_html = scrapy.Field()
    damage = scrapy.Field()
    cost = scrapy.Field()
    type = scrapy.Field()
    race = scrapy.Field()
    rarity = scrapy.Field()
    errata = scrapy.Field()
    keywords = scrapy.Field()
    valid_formats = scrapy.Field()
