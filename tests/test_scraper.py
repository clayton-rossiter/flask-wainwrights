import requests

import pandas as pd

from .framework import Framework

from main import scrape
from src.scraper import Scraper, WainwrightTables


class TestWainWrightTable(Framework):

    def setUp(self):
        super().setUp()
        self.tables = WainwrightTables

    def test_wainwrights_table_included(self):
        """check wainwright fells table ID is recorded"""
        self.assertTrue(WainwrightTables.fells.value, 1)

    def test_outlying_table_included(self):
        """check outlying fells table ID is recorded"""
        self.assertTrue(WainwrightTables.outlying_fells.value, 2)


class TestScraper(Framework):

    def setUp(self):
        super().setUp()
        self.scraper = Scraper()


    def test_url_still_exists(self):
        """check the main url for scraping still exists"""
        r = requests.get(self.scraper.url)
        self.assertTrue(r.status_code, 200)

    def test_fells_and_outlying_fells_downloaded(self):
        """checks the fells and outlying fells are populated from the valid url"""
        self.scraper.scrape_wikipedia()
        self.assertIsInstance(self.scraper.fells, pd.DataFrame)
        self.assertIsInstance(self.scraper.outlying_fells, pd.DataFrame)

        self.assertEqual(self.scraper.fells.index.stop, 214)
        self.assertEqual(self.scraper.outlying_fells.index.stop, 116)

    def test_longitude_and_latitude_populated(self):
        """check longitude and latitude are correctly appended from grid references"""
        self.scraper.longitude=[]
        self.scraper.latitude=[]
        self.scraper.scrape_wikipedia()
        self.scraper.convert_grid_references()
        df = self.scraper.append_df()
        self.assertIn('Longitude', df.columns.tolist())
        self.assertIn('Latitude', df.columns.tolist())


class TestMainScrape(Framework):

    def setUp(self):
        super().setUp()

    def test_fells_scraped_from_main_url(self):
        """checks all wainwright fells are scraped from main url"""
        df = scrape()
        self.assertEqual(df.index.stop, 214)
        self.assertIn('Longitude', df.columns.tolist())
        self.assertIn('Latitude', df.columns.tolist())

    