import schedule
import time
import os

def run_main_script():
    os.system("python main.py")

# Planifie l'exécution tous les jours à 9h00
schedule.every().day.at("09:00").do(run_main_script)

print("⏳ Scheduler actif... Appuyez sur CTRL+C pour arrêter.")
while True:
    schedule.run_pending()
    time.sleep(60)
