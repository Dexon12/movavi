import time
import uuid

from typing import Callable, Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor as APSchedulerThreadPoolExecutor
from apscheduler.executors.pool import ProcessPoolExecutor as APSchedulerProcessPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore

from app.utils.helpers import ParserUtils
from global_config import settings


class Scheduler:
    def __init__(self):
        self.__aps_executors = {
            'default': APSchedulerThreadPoolExecutor(max_workers=settings.MAX_INSTANCES),
            'processpool': APSchedulerProcessPoolExecutor(max_workers=settings.MAX_INSTANCES)
        }

        self.__aps_jobstores = {
            'default': MemoryJobStore()
        }

        self.__aps_job_defaults = {
            'coalesce': False,
            'max_instances': settings.MAX_INSTANCES
        }

        self.scheduler = BackgroundScheduler(
            jobstores=self.__aps_jobstores,
            executors=self.__aps_executors,
            job_defaults=self.__aps_job_defaults,
            timezone="UTC"
        )
        self.scheduler.start()

    def process_task(self, entry: dict, task: Callable[..., Any]):
        id_ = entry["id"]
        email = entry["email"]
        proxy = entry["proxy"]

        try:
            result = task(email=email, proxy=proxy)
            print(f"[CHECKER RESULT]: Result with id - {id_} is {result}")

            result_data = {
                "id": id_,
                "email": email,
                "result": result
            }
            ParserUtils.write_result_to_json(result_data)
        except Exception as e:
            print(f"Error while processing email {email}: {e}")

    def schedule_tasks(self, task: Callable[..., Any]):
        data = ParserUtils.read_csv(settings.CSV_FILE_NAME)
        for entry in data:
            if not ParserUtils.validate_email(entry["email"]):
                print("[TASK]: Email is not valid!")
                return
            
            job_id = f"checker_{entry['id']}_{uuid.uuid4()}"
            self.scheduler.add_job(
                self.process_task,
                args=[entry, task],
                id=job_id,
                replace_existing=False,
                misfire_grace_time=60
            )
            print(f"[SCHEDULER]: Scheduled job {job_id} for entry ID {entry['id']}")

    def run_forever(self):
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    def stop(self):
        self.scheduler.shutdown()
        print("[SCHEDULER]: Scheduler shut down successfully!")
