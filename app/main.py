from typing import Optional

from app.parser.logic import MovaviParse
from app.utils.scheduler import Scheduler


def checker(email: str, proxy: str) -> Optional[bool]:
    checker = MovaviParse(email=email, proxy=proxy)
    return checker.checker()

if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.schedule_tasks(checker)
    scheduler.run_forever()
    