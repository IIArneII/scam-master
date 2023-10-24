import asyncio
from pyppeteer import launch, browser as pypp_browser, page as pypp_page
from scam_master.services.models.errors import TRANSACTION_ALREADY_EXISTS
from scam_master.services.models.transactions import Transaction

class Browser:
    def __init__(self, transaction: Transaction, browser: pypp_browser.Browser, page: pypp_page.Page):
        self.transaction: Transaction = transaction
        self.browser: pypp_browser.Browser = browser
        self.page: pypp_page.Page = page

_pool: dict[str, Browser] = {}
_pool_lock: asyncio.Lock = asyncio.Lock()

async def start_browser(transaction: Transaction) -> Browser:
    async with _pool_lock:
        if _pool.get(transaction.transaction_id):
            raise TRANSACTION_ALREADY_EXISTS
    
    browser: pypp_browser.Browser = await launch(headless=False, defaultViewport=False, width=1920, height=1080)
    page: pypp_page.Page = (await browser.pages())[0]
    
    await page.evaluateOnNewDocument('''
        () => {
            // Pass the Webdriver test
            Object.defineProperty(navigator, "webdriver", {
                get: () => false,
            });

            // Pass the Chrome Test
            window.navigator.chrome = {
                runtime: {},
            };

            // Add permissions
            const originalQuery = window.navigator.permissions.query;
            return window.navigator.permissions.query = (parameters) => (
                parameters.name === "notifications" ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );

            // Pass the plugins length check
            Object.defineProperty(navigator, "plugins", {
                get: () => [1, 2, 3, 4, 5],
            });

            // Pass the languages check
            Object.defineProperty(navigator, "languages", {
                get: () => ["en-US", "en"],
            });
        }
    ''')

    br: Browser = Browser(transaction, browser, page)

    async with _pool_lock:
        _pool[transaction.transaction_id] = br

    asyncio.get_event_loop().call_later(350, asyncio.create_task, stop_browser(transaction.transaction_id))

    return br

async def get_browser(transaction_id: str) -> Browser | None:
    async with _pool_lock:
        return _pool.get(transaction_id)

async def stop_browser(transaction_id: str) -> None:
    async with _pool_lock:
        if transaction_id in _pool:
            await _pool[transaction_id].browser.close()
            del _pool[transaction_id]
