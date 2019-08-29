from crontab import CronTab
import os

cron = CronTab(tabfile=os.path.join(os.getcwd(), "face", "filename.tab"))
job = cron.new(command="python uploaddataset.py")
# job.hour.every(7)
job.minute.every(1)

# job.every_reboot()
cron.write()

