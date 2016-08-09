from selenium import webdriver
import sys
import time
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from unittest import skip
# import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase




class FunctionalTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		print ("setUp is called");
		self.browser = create_browser()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		print("tearDown is called")
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

def create_browser():
	return webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])#Chrome('/home/suraj/Downloads/chromedriver')

