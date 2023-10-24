from asyncio import Lock, get_event_loop, create_task
from pyppeteer import launch
from pyppeteer.page import Page as PyppPage
from pyppeteer.browser import Browser as PyppBrowser

from scam_master.services.models.errors import TRANSACTION_ALREADY_EXISTS
from scam_master.infrastructure.helpers.java_scripts import stealth_plugin
from scam_master.services.models.transactions import Transaction


class Browser:
    def __init__(self, transaction: Transaction, page: PyppPage):
        self.transaction: Transaction = transaction
        self.page: PyppPage = page


class BrowserManager:
    def __init__(self) -> None:
        self._pool: dict[str, Browser] = {}
        self._pool_lock: Lock = Lock()
    
    async def start(self, transaction: Transaction, timeout: int = 350) -> Browser:
        async with self._pool_lock:
            if self._pool.get(transaction.transaction_id):
                raise TRANSACTION_ALREADY_EXISTS
        
        browser: PyppBrowser = await launch(headless=False, defaultViewport=False, width=1920, height=1080)
        page: PyppPage = await browser.newPage()
        
        await page.evaluateOnNewDocument(stealth_plugin)

        br = Browser(transaction, page)

        async with self._pool_lock:
            self._pool[transaction.transaction_id] = br

        get_event_loop().call_later(timeout, create_task, self.stop(transaction.transaction_id))

        return br
    
    async def get(self, transaction_id: str) -> Browser | None:
        async with self._pool_lock:
            return self._pool.get(transaction_id)

    async def stop(self, transaction_id: str) -> None:
        async with self._pool_lock:
            if transaction_id in self._pool:
                await self._pool[transaction_id].page.browser.close()
                del self._pool[transaction_id]
