import psutil
import requests
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime
import os

logging.basicConfig(
    filename='logs/monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_service_health():
    try:
        # Vérifier l'API
        response = requests.get('https://votre-domaine.com/health')
        if response.status_code != 200:
            alert("API Health Check Failed", f"Status code: {response.status_code}")
            return False
        
        # Vérifier l'utilisation CPU/RAM
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        if cpu_percent > 90 or memory.percent > 90:
            alert("Resource Usage Alert", 
                  f"CPU: {cpu_percent}%, Memory: {memory.percent}%")
            return False
        
        # Vérifier l'espace disque
        disk = psutil.disk_usage('/')
        if disk.percent > 90:
            alert("Disk Space Alert", f"Disk usage: {disk.percent}%")
            return False
            
        return True
        
    except Exception as e:
        alert("Monitoring Error", str(e))
        return False

def alert(subject, message):
    logging.error(f"{subject}: {message}")
    # Envoyer email d'alerte
    # ... configuration email ...

if __name__ == "__main__":
    check_service_health() 