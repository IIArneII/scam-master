from pyppeteer.page import Page as PyppPage

stealth_plugin = '''
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
'''

async def apply_stealth(page: PyppPage):
    # Pass the User-Agent Test
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    # Pass the Webdriver Test
    await page.evaluateOnNewDocument('() => { Object.defineProperty(navigator, "webdriver", { get: () => undefined }) }')

    # Pass the Chrome Test
    await page.evaluateOnNewDocument('() => { window.navigator.chrome = { runtime: {}, }; }')

    # Pass the Permissions Test
    await page.evaluateOnNewDocument('() => { const originalQuery = window.navigator.permissions.query; return window.navigator.permissions.query = (parameters) => (parameters.name === "notifications" ? Promise.resolve({ state: Notification.permission }) : originalQuery(parameters)); }')

    # Pass the Plugins Length Test
    await page.evaluateOnNewDocument('() => { Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3, 4, 5], }); }')

    # Pass the Languages Test
    await page.evaluateOnNewDocument('() => { Object.defineProperty(navigator, "languages", { get: () => ["en-US", "en"], }); }')
    
    await page.evaluateOnNewDocument('''() => {
        let pluginData = [
            { name: "Chrome PDF Plugin", filename: "internal-pdf-viewer" },
            { name: "Chrome PDF Viewer", filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai" },
            { name: "Native Client", filename: "internal-nacl-plugin" }
        ];
        Object.defineProperty(navigator, "plugins", {
            get: () => pluginData,
        });
    }''')

    # Pass the iframe Test
    await page.evaluateOnNewDocument('''() => {
        Object.defineProperty(HTMLIFrameElement.prototype, "contentWindow", {
            get: function() {
                return window;
            }
        });
    }''')

    # Pass toString test, though it breaks JS functionalities, use with caution
    await page.evaluateOnNewDocument('''() => {
        window.navigator.chrome = { runtime: {} };
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications'
                ? Promise.resolve({ state: Notification.permission })
                : originalQuery(parameters)
        );
        const getParameter = WebGLRenderingContext.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === 37445) {
                return 'NVIDIA Corporation';
            }
            if (parameter === 37446) {
                return 'NVIDIA GeForce GTX 1050 Ti with Max-Q Design/PCIe/SSE2';
            }
            return getParameter(parameter);
        };
    }''')

    # Mocking WebGL vendor and renderer
    await page.evaluateOnNewDocument('''() => {
        const getParameter = WebGLRenderingContext.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            // UNMASKED_VENDOR_WEBGL
            if (parameter === 37445) {
                return 'NVIDIA Corporation';
            }
            // UNMASKED_RENDERER_WEBGL
            if (parameter === 37446) {
                return 'NVIDIA GeForce GTX 1050 Ti with Max-Q Design/PCIe/SSE2';
            }
            return getParameter(parameter);
        };
    }''')

    # Mocking battery status API
    await page.evaluateOnNewDocument('''() => {
        const getBattery = Navigator.prototype.getBattery;
        Navigator.prototype.getBattery = async () => {
            const battery = await getBattery.call(navigator);
            return Object.defineProperties(battery, {
                chargingTime: {
                    get: () => Infinity,
                },
                dischargingTime: {
                    get: () => Infinity,
                },
                level: {
                    get: () => 0.5,
                },
                charging: {
                    get: () => true,
                },
            });
        };
    }''')
