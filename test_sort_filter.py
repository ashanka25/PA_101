# Import selenium modules
# Import fixture from conftest
# Load testbed configs values

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from conftest import *
from config import TestConfig

# This is the test data to validate sorting and filtering test
# The testdata is a list of tuples
# First element of tuple: Provide the string to filter with; can be empty string for no filtering
# Second element of tuple: Column to sory by; choose from name, cases, complexity, averageImpact

testdata = [
    ("", "ffhhjjjk"),
    ("", "name"),
    ("p", "cases"),
    ("M", "averageImpact"),
    ("k","ffffg"),
    ("", "complexity"),
    ("y", "name"),
    ("fhgiiogjhkhlhjhkhkhkhjhjgh", "complexity"),
    (" ", "complexity"),
]


#Loading the fixture
@pytest.mark.usefixtures("load_app_data")
class Test():

    #parametrising the function to run the below tests for all values in testdata
    @pytest.mark.parametrize("filter_string,sorting_val", testdata)
    def test_sorting_and_filtering(self,filter_string, sorting_val):
        if sorting_val in ('cases','name','averageImpact','complexity'):
          self.driver.refresh()
          self.driver.implicitly_wait(1)
          self.driver.find_element_by_id("filter-input").clear()
          self.driver.find_element_by_id("filter-input").send_keys(filter_string)

          dropdown = Select(self.driver.find_element_by_id("sort-select"))
          dropdown.select_by_value(sorting_val)
          selected_table = get_table_value(self.driver)

          assert equiv(selected_table, sort_and_filter(self.master_data, filter_string, sorting_val),
                     TestConfig.sort_field_map[sorting_val])
        else:
            pytest.skip("Skipping test: Sort field not valid: {0}".format(sorting_val))

