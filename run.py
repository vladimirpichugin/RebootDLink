# -*- coding: utf-8 -*-
# Author: Vladimir Pichugin <vladimir@pichug.in>
import time
import schedule

import main


if __name__ == "__main__":
    schedule.every().day.at(str(main.config.get('AutoReboot', 'Hour'))).do(main.run_threaded, name='AutoReboot', func=main.reboot)

    # Поддерживать работу основной программы, пока бот работает.
    while True:
        try:
            if not schedule.get_jobs():
                print("Schedule jobs not found, shutting down..")
                break

            schedule.run_pending()

            time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down..")
            break
