# Test configuration file for Kamile Sor automation tests (Playwright)

BASE_URL = "https://kamilesor.com"
HEADLESS = False  # True for headless mode
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
SLOW_MO = 0  # Milliseconds delay between actions (for debugging)

# Timeouts (in milliseconds)
IMPLICIT_WAIT = 10000
EXPLICIT_WAIT = 15000
NAVIGATION_TIMEOUT = 30000

# Login information
LOGIN_USER = "inuglias@gmail.com"
LOGIN_PASSWORD = "2534.iollaH"

# Playwright specific settings
RECORD_VIDEO = False  # Video kayıt et
RECORD_TRACE = False  # Trace kayıt et (debugging için)


