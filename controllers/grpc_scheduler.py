import os.path
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED


class grpc_scheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.last_execution_time = self.get_last_execution_time()
        if self.last_execution_time:
            self.last_execution_time = datetime.datetime.fromisoformat(self.last_execution_time)

    def get_last_execution_time(self):
        filename = 'last_execution_time.txt'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return f.read()
        else:
            return None

    def save_last_execution_time(self):
        filename = 'last_execution_time.txt'
        with open(filename, 'w') as f:
            f.write(datetime.datetime.now().isoformat())

    def schedule_job(self, job, **kwargs):
        if self.last_execution_time:
            print("Scheduling")
            self.scheduler.add_job(
                job,
                'interval',
                **kwargs,
                next_run_time=self.last_execution_time
            )
        else:
            print("Scheduling")
            self.scheduler.add_job(
                job,
                'interval',
                **kwargs
            )
        self.scheduler.start()

    def on_job_executed(self, event):
        self.save_last_execution_time()

    def start(self, job, **kwargs):
        print("Starting scheduler")
        self.schedule_job(job, **kwargs)
        self.scheduler.add_listener(self.on_job_executed, EVENT_JOB_EXECUTED)

    def stop(self):
        self.scheduler.shutdown()
