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
