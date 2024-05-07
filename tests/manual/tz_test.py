from datetime import datetime

from pytz import timezone
now = datetime.now(timezone('Europe/Moscow'))
print(now.strftime('%D в %X'))
