from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.common.by import By
from pyppeteer.page import Page as PyppPage
from loguru import logger
from time import sleep

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.services.models.errors import UNKNOWN_TRANSFER_STATUS, BankError
from scam_master.services.models.transactions import Card


class OtpTransfer(IBankTransfer):
    '''
    Отпбанк.
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

            cookie = page.find_elements(By.XPATH, '/html/body/div[7]/div/a[2]')
            if cookie:
                cookie[0].click()

            frame = page.find_element(By.ID, 'p2pFrame')
            page.switch_to.frame(frame)

            sleep(2)

            card_inputs = page.find_elements(By.CSS_SELECTOR, 'input[type="tel"][data-vv-as="Номер карты"]')
            if len(card_inputs) != 2:
                raise UNKNOWN_TRANSFER_STATUS
            
            sender_card_input = card_inputs[0]
            recipient_card_input = card_inputs[1]
            
            sleep(2)

            sender_card_input.send_keys(sender_card.card_number)

            sleep(2)

            recipient_card_input.send_keys(recipient_card_number)

            sleep(2)

            cvc_input = page.find_element(By.NAME, 'src.csc')
            cvc_input.send_keys(sender_card.cvc)

            sleep(2)

            date_inputs = page.find_elements(By.CSS_SELECTOR, 'div.multiselect')
            if len(card_inputs) != 2:
                raise UNKNOWN_TRANSFER_STATUS
            
            month_select = date_inputs[0]
            year_select = date_inputs[1]
            month_text = sender_card.expiration_date[:2]
            year_text = sender_card.expiration_date[2:]

            sleep(2)

            OtpTransfer._date_field(month_select, month_text)

            sleep(2)

            OtpTransfer._date_field(year_select, year_text)

            sleep(2)

            transfer_amount = f'{(amount / 100):.2f}'
            amount_input = page.find_element(By.NAME, 'payment.amount')
            amount_input.click()
            amount_input.send_keys(transfer_amount)

            sleep(2)

            offer_checkbox = page.find_element(By.ID, 'offer-confirm-checkbox')
            if not offer_checkbox.is_selected():
                offer_checkbox.click()
            
            sleep(2)

            try:
                button = page.find_element(By.CSS_SELECTOR, 'div.col-12.col-md-6.order-last')
                button.click()
            except Exception:
                try:
                    button = page.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-block.mt-3')
                    button.click()
                except Exception:
                    raise

        except BankError:
            raise

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
            sleep(4)

            element = page.find_element(By.CSS_SELECTOR, 'h3.text-success')
            text = element.text

            logger.info(f'Transfer status: {text}')

            if 'Операция выполнена успешно' not in text:
                raise UNKNOWN_TRANSFER_STATUS
        
        except BankError:
            raise

        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS
    

    @staticmethod
    def _date_field(element: WebElement, text: str) -> None:
        select_number = element.find_element(By.XPATH, f'//span[text()="{text}"]')

        if not select_number.is_displayed():
            for_click = element.find_element(By.CSS_SELECTOR, 'div.multiselect__select')
            for_click.click()
            sleep(1)

        select_number.click()
