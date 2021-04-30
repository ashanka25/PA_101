
#Importing all necessary modules
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from config import TestConfig

##################################
# This is a pytest fixture to initiate the browser, load app url,
# and retrieve table data and close the webdriver after every test.
# This fixture is called before and after every test

@pytest.fixture(scope="class")
def load_app_data(request):
    '''
    This is a pytest fixture to initiate the browser, load app url,
    retrieve table data and close the driver at the end of every test
    :param request: To store and retrieve values across tests. This sets the
        webdriver and also retrieves and stores the master data of all records
        in the table.
    '''
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(TestConfig.app_url)
    request.cls.driver = driver
    request.cls.master_data = get_table_value(driver)
    yield
    driver.close()


def get_table_value(driver):
    '''
    This function retrieves all the table row data and builds a master table
    which is used for comparision later
    :param driver: webdriver handle
    :return: master_data: table with all original values before sorting or filtering
    '''

    #get all the rows
    rows = driver.find_elements_by_class_name("table-row")
    master_data = []

    #Insert data from the rows in to new table(master_data) row
    for row in rows:
        master_data_row = []
        row_data = row.find_elements_by_css_selector("[class*='table-data']")
        for element in row_data:
            master_data_row.append(element.text)

        #change everything to lowercase for first column
        master_data_row[0] = master_data_row[0].lower()

        #change everything in second column to converted multipliers
        num_of_cases = master_data_row[1]
        if num_of_cases[-1].upper() in TestConfig.multiplier_dict:
            num, mag = num_of_cases[:-1],num_of_cases[-1]
            num_of_cases = float(num) * TestConfig.multiplier_dict[mag.upper()]
        else:
            num_of_cases = float(num_of_cases)
        master_data_row[1] = num_of_cases

        #change everything in third column to floats
        master_data_row[2] = float(master_data_row[2])
        master_data.append(master_data_row)
    return master_data


def filter_by_value(l, val):
    '''
    This function returns a sorted table after filtering with val
    :param l: table (list of lists) to be filtered
    :param val: string to use as filter
    :return: filtered table (list of lists matching filter)
    '''
    val = val.lower()
    return list(filter(lambda x: val in x[0] or val in x[-1], l))


def sort_by_field(l, field="name"):
    '''
    This function returns a sorted table after sorting the data in original table
        using the provided field
    :param l: table (list of lists) to be sorted
    :param field: field to be sorted by
    :return: sorted table (list of lists sorted by field)
    '''
    if field is None:
        return l
    elif field == "complexity":
        return sorted(l, key=lambda x: TestConfig.complexity_map[x[TestConfig.sort_field_map[field]]])
    else:
        return sorted(l, key=lambda x: x[TestConfig.sort_field_map[field]])


def sort_and_filter(l,filter_text,sort_val):
    '''
    This function performs filter and sorting in conjunction
    :param l: list to be sorted and filtered
    :param filter_text: string to use as filter
    :param sort_val: field to be sorted by
    :return: sorted and filtered table (list of lists)
    '''
    filter_list = filter_by_value(l, filter_text)
    return sort_by_field(filter_list,sort_val)


def equiv(l1, l2, key):
    '''
    Check if two tables are equivalent given a column that is sorted.
    The function validates the sorting using the column next to the one being sorted.
    It assumes no order in the additional column being validated.
    :param l1: table1 (list of lists)
    :param l2: table2 (list of lists)
    :param key: key to sort both tables with
    :return: True if both lists are same, else False
    '''
    # Sets to store values from the additional column used for validation
    d1 = set()
    d2 = set()

    # The key of the column being used for validation
    nkey = (key + 1) % 4

    if len(l1) != len(l2):
        # Expected and actual tables have different number of rows
        return False

    for i in range(len(l1)):
        if l1[i][key] != l2[i][key]:
            # The sorting key is not identical in the expected and actual tables
            return False

        # Add the validation keys to the respective sets
        d1.add(l1[i][nkey])
        d2.add(l2[i][nkey])

    # Check if the validation keys of the expected and actual tables match
    return d1 == d2






