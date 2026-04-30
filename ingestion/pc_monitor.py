import psutil
import pygetwindow as gw
import time
import json
import os
from datetime import datetime
import threading

class PCMonitor: 
    def __init__(self, log_path="data/pc_activity.json"):
        self.log_path = log_path # Saved previous activity
        running = False # Currently is the monitor is active or not
        self.current_activity = {} # Captures the most recent activities
        os.makedirs("data", exist_ok=True) # Makes a data folder if not exits

        # If there are not any logs exists, then creates one empty []
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w") as f:
                json.dump([], f)
        
    def get_active_window(self):
        try:
            window = gw.getActiveWindow() # Talks to window and gets an object
            return window.title if window else "Unknown" # Fetching the object and checking the main title of the current task
        except:
            return "Unknown"
    
    """
    @returns - List like ["chrome.exe", "discord.exe", "Code.exe", "spotify.exe", "python.exe"]
    """
    def get_running_apps(self):
        apps = set() # Set to remove duplicate processes 
        for proc in psutil.process_iter(['name']): # Returns the name of active processes
            try:
                apps.add(proc.info['name'])
            except:
                pass
        return list(apps)

    def log_activity(self):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "active_window": self.get_active_window(), 
            "running_apps": self.get_running_apps()
        }

        self.current_activity = entry # Create a snapshot of the current activity 

        with open(self.log_path, "r") as f:
            logs = json.load(f)
        
        logs.append(entry)

        if len(logs) > 100:
            logs = logs[-100:] # Keeps the last 100 snapshots 
        
        with open(self.log_path, "w") as f:
            json.dump(logs, f, indent=2)
    
    def get_summary(self): # This is what gets fed to the machine. A summary. 
        if not self.current_activity:
            return "No activity tracked yet!"
        
        return (
            f"Active window: {self.current_activity.get('active_window', 'Unknown')}. "
            f"Currently running {len(self.current_activity.get('running_apps', []))} processes."
        )
    
    def _monitor_loop(self):
        while self.running: 
            self.log_activity()
            time.sleep(10)
    
    def start(self):
        self.running = True
        # This block is important. As this code will be running, Jarvis would wait for the running block infinitely. So we are shifting this in a separate thread.
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True) # daemon=True -> kills zombie process
        self.thread.start()
