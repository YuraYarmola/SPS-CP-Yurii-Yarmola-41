import psutil  # Для отримання інформації про систему
import time    # Для затримки між оновленнями даних


class SystemMonitor:
    def __init__(self):
        self.running = False

    def start_monitoring(self):
        self.running = True
        while self.running:
            self.update_system_info()
            time.sleep(1)

    def stop_monitoring(self):
        self.running = False

    def update_system_info(self):
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        print("\n===== System Monitoring =====")
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
        print(f"Disk Usage: {disk_usage}%")

    def set_thresholds(self):
        pass


class CPUUsageMonitor:
    def __init__(self):
        pass

    def get_cpu_usage(self):
        pass

    def notify_if_threshold_exceeded(self):
        pass


class MemoryUsageMonitor:
    def __init__(self):
        pass

    def get_memory_usage(self):
        pass

    def notify_if_threshold_exceeded(self):
        pass


class DiskSpaceMonitor:
    def __init__(self):
        pass

    def get_disk_space(self):
        pass

    def notify_if_threshold_exceeded(self):
        pass


class NetworkTrafficMonitor:
    def __init__(self):
        pass

    def get_network_traffic(self):
        pass

    def notify_if_threshold_exceeded(self):
        pass


class SystemEventMonitor:
    def __init__(self):
        pass

    def get_system_events(self):
        pass

    def notify_if_critical_event_detected(self):
        pass


class TemperatureAndFanMonitor:
    def __init__(self):
        pass

    def get_temperature_and_fan_info(self):
        pass

    def notify_if_threshold_exceeded(self):
        pass


class SystemInformation:
    def __init__(self):
        pass

    def get_basic_system_info(self):
        pass

    def get_installed_devices_info(self):
        pass

    def get_network_info(self):
        pass


class NotificationManager:
    def __init__(self):
        pass

    def send_notification(self):
        pass
