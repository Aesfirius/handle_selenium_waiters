from typing import List, Union

import concurrent.futures

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from appium.webdriver.common.mobileby import MobileBy

"""
    :param timeout: waiting timeout (default timeout=4)
    :param kwargs:

        for id use:
            by_id="value_id"

        for xpath use:
            by_xpath="xpath_value"

        for accessibility id use:
            accessibility_id="value_id"

        for predicate use:
            type="element_type", name="element_name", value="element_value"

            if needed you can use [contains | beginswith | endswith] like:
                type_contains="element_type", name_beginswith="element_name", value_endswith="element_value"

"""


def element_is_visible(driver, timeout: int = 4, **kwargs) -> bool:
    """
    :return: bool "True" | "False"

    :Usage:
    element_is_visible(driver, timeout=Your_Timeout, by_xpath="//Your/xpath")
    element_is_visible(driver, timeout=Your_Timeout, by_id="Your_ID")
    element_is_visible(driver, timeout=Your_Timeout, accessibility_id="Your_accessibility_id")
    element_is_visible(driver, timeout=Your_Timeout, type="element_type", name="element_name", value="element_value")
    element_is_visible(driver, timeout=Your_Timeout, type_contains="element_type",
                                                     name_beginswith="element_name",
                                                     value_endswith="element_value")

    """
    try:
        el = wait_condition(kwargs)
        wait = WebDriverWait(driver, timeout)
        wait.until(lambda wd: driver.find_element(el['by'], el['value']).is_displayed())
        return True
    except (NoSuchElementException, TimeoutException):
        return False


def element_is_not_visible(driver, timeout: int = 4, **kwargs) -> bool:
    """
    :return: bool "True" | "False"

    :Usage:
    element_is_not_visible(driver, timeout=Your_Timeout, by_xpath="//Your/xpath")
    element_is_not_visible(driver, timeout=Your_Timeout, by_id="Your_ID")
    element_is_not_visible(driver, timeout=Your_Timeout, accessibility_id="Your_accessibility_id")
    element_is_not_visible(driver, timeout=Your_Timeout, type="element_type", name="element_name", value="element_value")
    element_is_not_visible(driver, timeout=Your_Timeout, type_contains="element_type",
                                                         name_beginswith="element_name",
                                                         value_endswith="element_value")

    """
    try:
        el = wait_condition(kwargs)
        wait = WebDriverWait(driver, timeout)
        wait.until_not(lambda wd: driver.find_element(el['by'], el['value']).is_displayed())
        return True
    except TimeoutException:
        return False


def one_of_elements_is_visible(driver, timeout: int = 4, **kwargs) -> bool:
    """
    :return: bool "True" | "False"

    !!! separate by '; ' --> semicolon and whitespace !!!

    :Usage:
    one_of_elements_is_visible(driver, timeout=Your_Timeout, by_xpath="//Your/xpath; //Your/xpath2")
    one_of_elements_is_visible(driver, timeout=Your_Timeout, by_id="Your_ID; Your_ID_2")
    one_of_elements_is_visible(driver, timeout=Your_Timeout, accessibility_id="Your_accessib_id; Your_accessib_id_2")

    """
    vars_f = wait_condition(kwargs)
    by_ = vars_f['by']
    values = vars_f['value'].split('; ')
    exceptions = []
    for value_ in values:
        try:
            wait = WebDriverWait(driver, timeout)
            wait.until(lambda wd: driver.find_element(by_, value_).is_displayed())
            return True
        except (NoSuchElementException, TimeoutException) as e:
            exceptions.append(e)
    if len(exceptions) == len(values):
        return False


def get_element_with_timeout(driver, timeout: int = 4, **kwargs) -> Union[WebElement, Exception]:
    """
    :return: WebElement | Exception

    :Usage:
    get_element_with_timeout(driver, timeout=Your_Timeout, by_xpath="//Your/xpath").do_something()
    get_element_with_timeout(driver, timeout=Your_Timeout, by_id="Your_ID").do_something()
    get_element_with_timeout(driver, timeout=Your_Timeout, accessibility_id="Your_accessib_id").do_something()
    get_element_with_timeout(driver, timeout=Your_Timeout, type="element_type",
                                                           name="element_name",
                                                           value="element_value").do_something()
    get_element_with_timeout(driver, timeout=Your_Timeout, type_contains="element_type",
                                                         name_beginswith="element_name",
                                                         value_endswith="element_value").do_something()

    """
    try:
        el = wait_condition(kwargs)
        wait = WebDriverWait(driver, timeout)
        wait.until(
            lambda wd: driver.find_element(el['by'], el['value']).is_displayed() and
                       driver.find_element(el['by'], el['value']).is_enabled())
        return driver.find_element(el['by'], el['value'])
    except (NoSuchElementException, TimeoutException) as e:
        raise e


def get_elements_with_timeout(driver, timeout: int = 4, **kwargs) -> Union[List[WebElement], Exception]:
    """
    :return: [WebElement] | Exception

    :Usage:
    get_elements_with_timeout(driver, timeout=Your_Timeout, by_xpath="//Your/xpath")
    get_elements_with_timeout(driver, timeout=Your_Timeout, by_id="Your_ID")
    get_elements_with_timeout(driver, timeout=Your_Timeout, accessibility_id="Your_accessib_id")
    get_elements_with_timeout(driver, timeout=Your_Timeout, type="element_type",
                                                            name="element_name",
                                                            value="element_value")
    get_elements_with_timeout(driver, timeout=Your_Timeout, type_contains="element_type",
                                                            name_beginswith="element_name",
                                                            value_endswith="element_value")
    """
    try:
        el = wait_condition(kwargs)
        wait = WebDriverWait(driver, timeout)
        wait.until(lambda wd: driver.find_elements(el['by'], el['value']))
        return driver.find_elements(el['by'], el['value'])
    except (NoSuchElementException, TimeoutException) as e:
        raise e


def get_one_of_elements_with_timeout(driver, timeout: int = 4, **kwargs) -> Union[WebElement, Exception]:
    """
    :return: WebElement | Exception

    !!! separate by '; ' --> semicolon and whitespace !!!

    :Usage:
    get_one_of_elements_with_timeout(driver, timeout=Your_Timeout,
                                             by_xpath="//Your/xpath; //Your/xpath2").do_something()
    get_one_of_elements_with_timeout(driver, timeout=Your_Timeout, by_id="Your_ID; Your_ID_2").do_something()
    get_one_of_elements_with_timeout(driver, timeout=Your_Timeout,
                                             accessibility_id="Your_accessib_id; Your_accessib_id_2").do_something()
    """
    vars_f = wait_condition(kwargs)
    by_ = vars_f['by']
    values = vars_f['value'].split('; ')
    exceptions = []
    for value_ in values:
        try:
            wait = WebDriverWait(driver, timeout)
            wait.until(lambda wd: driver.find_element(by_, value_).is_displayed() and
                                  driver.find_element(by_, value_).is_enabled())
            return driver.find_element(by_, value_)
        except (NoSuchElementException, TimeoutException) as e:
            exceptions.append(e)
    if len(exceptions) == len(values):
        raise Exception(exceptions)


####################################################################################################
#                                                                                                  #
#        Async find element                                                                        #
#                                                                                                  #
####################################################################################################

def get_el(driver_, timeout_, by_, value_):
    try:
        wait = WebDriverWait(driver_, timeout_)
        wait.until(lambda wd: driver_.find_element(by_, value_).is_displayed() and driver_.find_element(by_,
                                                                                                        value_).is_enabled())
        return driver_.find_element(by_, value_)
    except (NoSuchElementException, TimeoutException) as e:
        return e


def get_one_of_elements_with_timeout_async(driver, timeout: int = 4, **kwargs) -> Union[WebElement, Exception]:
    """
    :return: WebElement | Exception

    !!! separate by '; ' --> semicolon and whitespace !!!

    :Usage:
    get_one_of_elements_with_timeout(driver, timeout=Your_Timeout,
                                             by_xpath="//Your/xpath; //Your/xpath2").do_something()
    get_one_of_elements_with_timeout(driver, timeout=Your_Timeout, by_id="Your_ID; Your_ID_2").do_something()
    get_one_of_elements_with_timeout(driver, timeout=Your_Timeout,
                                             accessibility_id="Your_accessib_id; Your_accessib_id_2").do_something()
    """
    exceptions = []
    result = None
    vars_f = wait_condition(kwargs)
    by = vars_f['by']
    values = vars_f['value'].split('; ')
    if len(values) > 0:
        with concurrent.futures.ThreadPoolExecutor(thread_name_prefix='selenium_find_el',
                                                   max_workers=len(values) + 1) as executor:
            futures = []
            for value in values:
                futures.append(executor.submit(get_el, driver, timeout, by, value))

            for future in concurrent.futures.as_completed(futures):
                try:
                    if isinstance(future.result(), WebElement):
                        result = future.result()
                        break
                except (NoSuchElementException, TimeoutException) as e:
                    exceptions.append(e)

    if len(exceptions) == len(values):
        raise Exception(exceptions)
    elif result is not None:
        return result


def wait_condition(kwargs) -> dict:
    if 'accessibility_id' in kwargs:
        by = MobileBy.ACCESSIBILITY_ID
        value = kwargs['accessibility_id']
    elif 'by_name' in kwargs:
        by = By.NAME
        value = kwargs['by_name']
    elif 'by_id' in kwargs:
        by = By.ID
        value = kwargs['by_id']
    elif 'by_xpath' in kwargs:
        by = By.XPATH
        value = kwargs['by_xpath']
    else:
        by = MobileBy.IOS_PREDICATE
        pre_value = []
        for x in kwargs:
            b = x.split("_")
            if len(b) > 1:
                pre_value.append('%s %s "%s"' % (b[0], b[1], kwargs[x]))
            else:
                pre_value.append('%s == "%s"' % (x, kwargs[x]))
        value = " AND ".join(i for i in pre_value)
    return {'by': by, 'value': value}
