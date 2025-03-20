import psutil
import GPUtil
import platform
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.system = platform.system()
        self.alerts = []
        
    def get_system_status(self):
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        status = f"System Status:\n"
        status += f"CPU Usage: {cpu_percent}%\n"
        status += f"Memory Usage: {memory.percent}%\n"
        status += f"Disk Usage: {disk.percent}%\n"
        
        try:
            gpus = GPUtil.getGPUs()
            for gpu in gpus:
                status += f"GPU Usage: {gpu.load*100}%\n"
                status += f"GPU Memory: {gpu.memoryUsed}/{gpu.memoryTotal} MB\n"
        except:
            pass
            
        return status

    def get_network_status(self):
        net_io = psutil.net_io_counters()
        return (f"Network Status:\n"
                f"Bytes Sent: {net_io.bytes_sent/1024/1024:.2f} MB\n"
                f"Bytes Received: {net_io.bytes_recv/1024/1024:.2f} MB")

    def monitor_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent']
                })
            except:
                pass
        return sorted(processes, key=lambda x: x['cpu'], reverse=True)[:5]
