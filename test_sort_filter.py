# Import selenium modules
# Import fixture from conftest
# Load testbed configs values

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from conftest import *
from config import TestConfig

# This is the test data to validate sorting and filtering test
# The testdata is a list of tuples
# first element of tuple: provide any strin g to filter with
# second element of tuple: sort by column. Provide any value from name,cases,complexity,averageImpact

testdata = [
    ("pa", "cases"),
    ("", "name"),
    ("p", "cases"),
    ("M", "averageImpact"),
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
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_id("filter-input").clear()
        self.driver.find_element_by_id("filter-input").send_keys(filter_string)

        dropdown = Select(self.driver.find_element_by_id("sort-select"))
        dropdown.select_by_value(sorting_val)
        selected_table = get_table_value(self.driver)
        self.driver.find_element_by_id("filter-input").send_keys(Keys.BACKSPACE*len(filter_string))

        assert equiv(selected_table, sort_and_filter(self.master_data, filter_string, sorting_val),
                     TestConfig.sort_field_map[sorting_val])

