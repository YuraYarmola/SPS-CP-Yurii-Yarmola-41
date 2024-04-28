import platform
import GPUtil
import psutil
import time
import WinTmp
import win32evtlog


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
        fans = psutil.sensors_fans()
        print("\n===== System Monitoring =====")
        print(f"CPU Usage: {cpu_usage}%")
        print(f"Memory Usage: {memory_usage}%")
        print(f"Disk Usage: {disk_usage}%")
        print(f"Fans Speed {fans}")

    def set_thresholds(self):
        pass


class CPUUsageMonitor:
    def get_cpu_count(self):
        """Get the number of logical CPUs."""
        return psutil.cpu_count()

    def get_cpu_frequency(self):
        """Get the current CPU frequency."""
        return psutil.cpu_freq()

    def get_cpu_utilization(self):
        """Get the current CPU utilization."""
        return psutil.cpu_percent()


class MemoryUsageMonitor:
    def __init__(self):
        pass

    @staticmethod
    def get_available_memory():
        """
        Get the available physical memory in bytes.
        """

        return psutil.virtual_memory().available

    @staticmethod
    def get_total_memory():
        """
        Get the available physical memory in bytes.
        """
        return psutil.virtual_memory().total

    @staticmethod
    def get_used_memory():
        """
        Get the used physical memory in bytes.
        """
        return psutil.virtual_memory().used

    @staticmethod
    def get_memory_usage_percentage():
        """
        Get the percentage of used physical memory.
        """
        return psutil.virtual_memory().percent


class DiskSpaceMonitor:
    def __init__(self):
        pass

    def get_all_disks(self):
        """
        Get a list of all disk partitions.
        """
        return psutil.disk_partitions(all=True)

    def get_disk_usage(self, disk):
        """
        Get disk usage information for a specific disk.
        """
        return psutil.disk_usage(disk)

    def get_all_disk_usage(self):
        """
        Get disk usage information for all disks.
        """
        all_disks = self.get_all_disks()
        disk_usage_info = {}
        for disk in all_disks:
            usage = self.get_disk_usage(disk.mountpoint)
            disk_usage_info[disk.mountpoint] = {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent

            }
        return disk_usage_info


class NetworkTrafficMonitor:
    def get_network_usage(self):
        net_stats = psutil.net_io_counters(pernic=True)
        networks = []
        for interface, stats in net_stats.items():
            networks.append({
                'Interface': interface,
                "Bytes send": stats.bytes_sent,
                "Bytes received": stats.bytes_recv,
                "Packets sent": stats.packets_sent,
                "Packets received": stats.packets_recv,
                "Error in/out": f"{stats.errin}/{stats.errout}",
                "Drop in/out": f"{stats.dropin}/{stats.dropout}",
            })
        return networks


class Temperature:

    def get_cpu_temperature(self):
        """ CPU temperature """
        return WinTmp.CPU_Temp()

    def get_gpu_temperature(self):
        """ GPU temperature """
        return WinTmp.GPU_Temp()


class SystemInformation:

    def get_basic_system_info(self):
        system_info = {'Platform': platform.platform(), 'Architecture': " ".join(platform.architecture()),
                       'System_name': platform.system() + " " + platform.release(), 'Version': platform.version(),
                       'Machine': platform.machine(), 'Processor': platform.processor(),
                       'Cpu Count': psutil.cpu_count(),
                       "Ram Size": str(round(psutil.virtual_memory().total / 1024**3, 2)) + " GB",
                       }

        gpus = GPUtil.getGPUs()
        for index, gpu in enumerate(gpus):
            system_info[f'GPU {index}'] = gpu.name

        return system_info

    def get_event_logs(self, total_logs=50, logtype="System"):
        print(logtype)
        server = None  # None implies local machine
        hand = win32evtlog.OpenEventLog(server, logtype)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = 0
        logs = []
        try:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            while events:
                for event in events:

                    logs.append(
                        {"Event ID": event.EventID,
                            "Time": event.TimeGenerated,
                         "Source Name": event.SourceName,

                         "Message": str(event.StringInserts),
                         }
                    )
                    if total > total_logs:
                        break
                    total += 1
                if total > total_logs:
                    break
                events = win32evtlog.ReadEventLog(hand, flags, 0)
        finally:
            win32evtlog.CloseEventLog(hand)
        return logs


class Processes:
    def get_processes(self):
        processes = []
        for process in psutil.process_iter():
            try:
                # Get process details
                process_info = {
                    'pid': process.pid,
                    'name': process.name(),
                    'cpu_percent': process.cpu_percent(),
                    "memory": process.memory_info().rss / 1024 / 1024,
                }
                processes.append(process_info)

            except psutil.Error:
                pass
        return processes