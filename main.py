from functions import *


if __name__ == "__main__":
    system_monitor = SystemMonitor()
    system_monitor.start_monitoring()

    cpu_monitor = CPUUsageMonitor()
    memory_monitor = MemoryUsageMonitor()

    while True:
        cpu_usage = cpu_monitor.get_cpu_usage()
        memory_usage = memory_monitor.get_memory_usage()

        cpu_monitor.notify_if_threshold_exceeded()
        memory_monitor.notify_if_threshold_exceeded()

    system_monitor.stop_monitoring()