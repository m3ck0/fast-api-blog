from rq import Worker


class BaseDeathPenalty(object):
    def __init__(self, *_, **__):
        pass

    def __enter__(self, *_, **__):
        pass

    def __exit__(self, *_, **__):
        pass


class BasicWindowsWorker(Worker):
    death_penalty_class = BaseDeathPenalty

    def main_work_horse(self, *_, **__):
        raise NotImplementedError("Test worker does not implement this method")

    def execute_job(self, *_, **__):
        """Execute job in same thread/process, do not fork()"""
        return self.perform_job(*_, **__)