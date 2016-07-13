from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		print ("setUp is called");
		self.browser = webdriver.Chrome("/home/suraj/Downloads/chromedriver")
		self.browser.implicitly_wait(3)

	def tearDown(self):
		print("tearDown is called")
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Suraj goes to check out the homepage of our app
		self.browser.get('http://localhost:8000')

		# He notices the page title and header mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		self.fail("error message")

if __name__ == '__main__':
	unittest.main(warnings='ignore')