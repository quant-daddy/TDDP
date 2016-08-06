from selenium import webdriver
from .base import FunctionalTest
import sys
import time
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from unittest import skip
# import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase




class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# Julia goes to the home page
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024,768)

		# She notices that the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
				inputbox.location['x'] + inputbox.size['width']/2, 
				512, 
				delta=5
			)

		# She starts a new list and sees the input is nicely centered there too
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
				inputbox.location['x']+inputbox.size['width']/2,
				512,
				delta=5
			)