# -*- coding: utf-8 -*-
import scrapy
import json
import requests
import shutil
import os
import io
import errno
import wget
from PIL import Image
from unicodedata import normalize
from tcg_helper_scrapy.items import MylItem


class MylSpider(scrapy.Spider):
    name = 'myl'
    allowed_domains = ['api.myl.cl']
    card_image_base_url = 'https://api.myl.cl/static/cards/{}/{}.jpg'
    card_detail_base_url = 'https://api.myl.cl/cards/profile/{}/{}'
    start_urls = [
        'https://api.myl.cl/cards/edition/terrores-nocturnos',
        ''
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
            valid_formats=response_json['valid_formats']
        )
        self.download_image(
            edition, response_json['details']['edid'])

    def download_image(self, edition_id, card_edition_id):
        url = self.card_image_base_url.format(edition_id, card_edition_id)
        filename = f'images/{edition_id}-{card_edition_id}.jpg'
        response = requests.get(url, verify=False)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        image_file = io.BytesIO(response.content)
        image = Image.open(image_file).convert('RGB')
        with open(filename, 'wb') as out_file:
            image.save(out_file, 'JPEG', quality=85)
        del response
