from asyncio import Lock, get_event_loop, create_task
from pyppeteer import launch
from pyppeteer.page import Page as PyppPage
from pyppeteer.browser import Browser as PyppBrowser
from pyppeteer_stealth import stealth
from loguru import logger

from scam_master.infrastructure.helpers.java_scripts import apply_stealth
from scam_master.services.models.transactions import Transaction
from config import BrowserConfig


class Browser:
    def __init__(self, transaction: Transaction, page: PyppPage):
        self.transaction: Transaction = transaction
        self.page: PyppPage = page


class BrowserManager:
    def __init__(self, browser_config: dict) -> None:
        self._config = BrowserConfig(browser_config)
        self._pool: dict[str, Browser] = {}
        self._pool_lock: Lock = Lock()
    
    async def start(self, transaction: Transaction, timeout: int = 350) -> Browser:
        async with self._pool_lock:
            if transaction.id in self._pool:
                    self.stop(transaction.id)
        
        browser: PyppBrowser = await launch(
            executablePath=self._config.PATH if self._config.PATH else None,
            headless=False,
            defaultViewport=False,
            width=1920,
            height=1080,
            dumpio=True,
            args=['--no-sandbox', '--disable-dev-shm-usage', '--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
        )
        page: PyppPage = await browser.newPage()
        
        await stealth(page)

        br = Browser(transaction, page)

        async with self._pool_lock:
            self._pool[transaction.id] = br

        get_event_loop().call_later(timeout, create_task, self.stop(transaction.id))

        logger.info(f'Create transaction {transaction.id}')
        return br
    
    async def get(self, transaction_id: str) -> Browser | None:
        async with self._pool_lock:
            return self._pool.get(transaction_id)

    async def stop(self, transaction_id: str) -> None:
        async with self._pool_lock:
            if transaction_id in self._pool:
                logger.info(f'Delete transaction {transaction_id}')
                await self._pool[transaction_id].page.browser.close()
                del self._pool[transaction_id]
