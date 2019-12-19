# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import shutil
import os
import io
import errno
import urllib
import ssl
from PIL import Image
from unicodedata import normalize
from tcg_helper_scrapy.items import MylItem

ssl._create_default_https_context = ssl._create_unverified_context

class MylSpider(scrapy.Spider):
    name = 'myl'
    allowed_domains = ['api.myl.cl']
    card_image_base_url = 'https://api.myl.cl/static/cards/{}/{}.png'
    card_detail_base_url = 'https://api.myl.cl/cards/profile/{}/{}'
    start_urls = [
        'https://api.myl.cl/cards/edition/invasion-oscura',
        'https://api.myl.cl/cards/edition/terrores-nocturnos',
        'https://api.myl.cl/cards/edition/tinta-inmortal',
        'https://api.myl.cl/cards/edition/arsenal',
        'https://api.myl.cl/cards/edition/kilimanjaro',
        'https://api.myl.cl/cards/edition/calavera',
        'https://api.myl.cl/cards/edition/olimpia',
        'https://api.myl.cl/cards/edition/dharma',
        'https://api.myl.cl/cards/edition/kemet',
        'https://api.myl.cl/cards/edition/legado-gotico',
        'https://api.myl.cl/cards/edition/hijos-del-sol',
    ]

    def create_card_detail_base_url(self, edition, slug):
        return self.card_detail_base_url.format(edition, slug)

    def create_card_image_url(self, edition_id, card_id):
        return self.card_image_base_url.format(edition_id, card_id)

    def parse(self, response):
        response_json = json.loads(response.body)
        edition = response.url.split('/')[-1]
        for card in response_json['cards']:
            yield scrapy.Request(url=self.create_card_detail_base_url(edition, card['slug']), callback=self.parse_card_detail)

    def parse_card_detail(self, response):
        response_json = json.loads(response.body)
        details = response_json['details']
        details.pop('illustrator')
        details.pop('visits')
        details.pop('flags')
        edition = details.pop('edition')
        yield MylItem(
            **response_json['details'],
            errata=response_json['errata'],
            valid_formats=response_json['valid_formats'],
            edition_id=response_json['edition']['id'],
            file_urls=[self.card_image_base_url.format(edition, response_json['details']['edid'])]
        )
