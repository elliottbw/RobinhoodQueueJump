import jump

REFERRAL_CODE = "XXXX"
BINARY_LOCATION = r"C:\Program Files\Mozilla Firefox\firefox.exe"
GECKO_DRIVER_LOCATION = r"C:\Program Files\Mozilla Firefox\geckodriver.exe"

queue_bot = jump.QueueJumpBot(BINARY_LOCATION, GECKO_DRIVER_LOCATION)
queue_bot.load_robinhood(REFERRAL_CODE)

while True:
    queue_bot.commit_referral(queue_bot.generate_random_email())
