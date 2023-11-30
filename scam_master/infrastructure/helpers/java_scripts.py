from selenium.webdriver import Chrome as Driver

from selenium_stealth.chrome_app import chrome_app
from selenium_stealth.chrome_runtime import chrome_runtime
from selenium_stealth.iframe_content_window import iframe_content_window
from selenium_stealth.media_codecs import media_codecs
from selenium_stealth.navigator_languages import navigator_languages
from selenium_stealth.navigator_permissions import navigator_permissions
from selenium_stealth.navigator_plugins import navigator_plugins
from selenium_stealth.navigator_vendor import navigator_vendor
from selenium_stealth.navigator_webdriver import navigator_webdriver
from selenium_stealth.user_agent_override import user_agent_override
from selenium_stealth.utils import with_utils
from selenium_stealth.webgl_vendor import webgl_vendor_override
from selenium_stealth.window_outerdimensions import window_outerdimensions
from selenium_stealth.hairline_fix import hairline_fix


def selenium_stealth(
        driver: Driver,
        languages: [str] = ["en-US", "en"],
        vendor: str = "Google Inc.",
        webgl_vendor: str = "Intel Inc.",
        renderer: str = "Intel Iris OpenGL Engine",
        fix_hairline: bool = False,
        run_on_insecure_origins: bool = False, **kwargs) -> None:
    if not isinstance(driver, Driver):
        raise ValueError("driver must is selenium.webdriver.Chrome, currently this lib only support Chrome")

    ua_languages = ','.join(languages)

    with_utils(driver, **kwargs)
    chrome_app(driver, **kwargs)
    chrome_runtime(driver, run_on_insecure_origins, **kwargs)
    iframe_content_window(driver, **kwargs)
    media_codecs(driver, **kwargs)
    navigator_languages(driver, languages, **kwargs)
    navigator_permissions(driver, **kwargs)
    navigator_plugins(driver, **kwargs)
    navigator_vendor(driver, vendor, **kwargs)
    navigator_webdriver(driver, **kwargs)
    # \/ Throws an exception \/
    # user_agent_override(driver, user_agent, ua_languages, platform, **kwargs)
    # /\ Throws an exception /\
    webgl_vendor_override(driver, webgl_vendor, renderer, **kwargs)
    window_outerdimensions(driver, **kwargs)

    if fix_hairline:
        hairline_fix(driver, **kwargs)
