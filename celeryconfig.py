from celery.schedules import crontab
from scheduler import  schedule_the_pass, modified_schedule
from datetime import timedelta
broker_url='redis://localhost:6379/0'
result_backend='redis://localhost:6379/0'

timezone='Asia/Kolkata'
enable_utc=False
pass_start_time, pass_end_time= modified_schedule()
t_initialize_pass = pass_start_time - timedelta(minutes=10)
t_generate_text_files = pass_start_time - timedelta(minutes=9)
t_switch_on_hydra = pass_start_time - timedelta(minutes=8)
t_switch_on_arduinos = pass_start_time - timedelta(minutes=4)
t_run_radio = pass_start_time - timedelta(minutes=3)
t_start_controllers = pass_start_time - timedelta(minutes=1)
t_kill_pid = pass_end_time + timedelta(minutes=1)
t_switch_off_gpio = pass_end_time + timedelta(minutes=2)
beat_schedule={
    'switch-on-gpio-pins': {
        'task': 'tasks.initiate_pass',
        'schedule':crontab(minute=t_initialize_pass.minute, hour=t_initialize_pass.hour),
    }, 
    'generate-text-files': {
        'task': 'tasks.generate_the_text_files',
        'schedule':crontab(minute=t_generate_text_files.minute, hour=t_generate_text_files.hour),
    },
    'switch-on-hydra': {
        'task': 'tasks.switch_on_hydra',
        'schedule':crontab(minute=t_switch_on_hydra.minute, hour=t_switch_on_hydra.hour),
    },
    'switch-on-arduinos': {
        'task': 'tasks.switch_on_arduinos',
        'schedule':crontab(minute=t_switch_on_arduinos.minute, hour=t_switch_on_arduinos.hour),
    },
    'start-radio': {
        'task': 'tasks.start_radio',
        'schedule':crontab(minute=t_run_radio.minute, hour=t_run_radio.hour),
    },
    'start-controllers': {
        'task': 'tasks.start_controllers',
        'schedule':crontab(minute=t_start_controllers.minute, hour=t_start_controllers.hour),
    },
    'switch-off-arduinos': {
        'task': 'tasks.switch_off_arduinos',
        'schedule':crontab(minute=pass_end_time.minute, hour=pass_end_time.hour),
    },
    'kill-pids': {
        'task': 'tasks.kill_pids',
        'schedule':crontab(minute=t_kill_pid.minute, hour=t_kill_pid.hour),
    },
     'switch-off-gpios': {
        'task': 'tasks.switch_off_gpio',
        'schedule':crontab(minute=t_switch_off_gpio.minute, hour=t_switch_off_gpio.hour),
    },
}

