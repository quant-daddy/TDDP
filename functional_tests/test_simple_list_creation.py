from selenium import webdriver
from .base import FunctionalTest, create_browser
import sys
import time
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from unittest import skip
# import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewVisitorTest(FunctionalTest):

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Julia heard abut a cool new To-Do App and goes online to check out the homepage of our app
		self.browser.get(self.server_url)

		# She notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do item straight away
		inputbox = self.get_item_input_box()
		self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

		# She types "buy peacock feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')

		# When she hits enter, the page updates, and now the page lists 
		# "1: Buy peacock feathers" as an item in a to-do list table
		inputbox.send_keys(Keys.ENTER)
		julia_list_url = self.browser.current_url
		self.assertRegex(julia_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly"
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)


		# The page updates again, and now shows both the items on her list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		
		# Now a new user, Francis, comes along to the site

		## We use a new browser session to make sure that no information 
		## of Julia's is coming along through cookies etc. 

		self.browser.quit()
		self.browser = create_browser()

		# Francis visits the home page. There is no sign of Julia's list
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)

		# Francis start a new list by entering a new item. He is less interesting than Julia
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)

		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, julia_list_url)

		# Again there is no trace of Julia's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)

		# Satisfies they both go back to drugs