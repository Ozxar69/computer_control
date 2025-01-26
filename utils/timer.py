
from datetime import datetime, timedelta


class Timer:
    def __init__(self):
        self.end_time = None
        self.timer_running = False

    def start_timer(self, minutes):

        self.end_time = datetime.now() + timedelta(minutes=minutes)
        self.timer_running = True

        return self.countdown()

    def countdown(self):
        while self.timer_running:
            remaining_time = self.end_time - datetime.now()
            if remaining_time.total_seconds() <= 0:
                self.timer_running = False
                break

            mins, secs = divmod(remaining_time.total_seconds(), 60)
            formatted_time = f"{int(mins):02}:{int(secs):02}"
            return formatted_time

    def check_timer(self):
        if self.timer_running:
            remaining_time = self.end_time - datetime.now()
            if remaining_time.total_seconds() > 0:
                mins, secs = divmod(remaining_time.total_seconds(), 60)
                formatted_time = f"{int(mins):02}:{int(secs):02}"
                return formatted_time
            else:
                return False
        else:
            return False


# Пример использования
timer = Timer()



