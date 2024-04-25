import clr
import psutil  # Для отримання інформації про систему
import time  # Для затримки між оновленнями даних
import GPUtil
import wmi

openhardwaremonitor_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer',
                               'Heatmaster', 'HDD']
cputhermometer_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']

openhardwaremonitor_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level',
                                   'Factor', 'Power', 'Data', 'SmallData']
cputhermometer_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level']


class Sensor:
    def __init__(self):
        self.sensors = {
            "Temperature": []
        }
        self.handle = self.__initialize_openhardwaremonitor()
        self.fetch_sensors(self.handle)

        # for key in self.sensors.keys():
        #     print(f"\n{key}:")
        #     for sensor in self.sensors[key]:
        #
        #         print(sensor.Hardware.Name, sensor.Hardware.HardwareType, sensor.Value)

    def __initialize_openhardwaremonitor(self):
        file = r'D:\LPNU\SEMESTR 6\SPZ\KURSOVA\SystemMonitor\SPS-CP-Yurii-Yarmola-41\OpenHardwareMonitorLib.dll'
        clr.AddReference(file)

        from OpenHardwareMonitor import Hardware

        handle = Hardware.Computer()
        handle.MainboardEnabled = True
        handle.CPUEnabled = True
        handle.RAMEnabled = True
        handle.GPUEnabled = True
        handle.HDDEnabled = True
        handle.Open()
        return handle

    def fetch_sensors(self, handle):
        for i in handle.Hardware:
            i.Update()
            for sensor in i.Sensors:

                if str(sensor.SensorType) in self.sensors.keys():
                    self.sensors[str(sensor.SensorType)].append(sensor)
                else:
                    self.sensors[str(sensor.SensorType)] = [sensor]

            for j in i.SubHardware:
                j.Update()
                for subsensor in j.Sensors:
                    if str(subsensor.SensorType) in self.sensors.keys():
                        self.sensors[str(subsensor.SensorType)].append(subsensor)
                    else:
                        self.sensors[str(subsensor.SensorType)] = [subsensor]

    def parse_sensor(self, sensor):
        if sensor.Value is not None:
            if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
                sensortypes = openhardwaremonitor_sensortypes
                hardwaretypes = openhardwaremonitor_hwtypes
                hardwaretypes = openhardwaremonitor_hwtypes
            else:
                return

            if 'Temperature' in str(sensor.SensorType):
                print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (
                    hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name,
                    sensor.Value))


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
    def __init__(self):
        pass

    def get_cpu_usage(self):
        pass

    def notify_if_threshold_exceeded(self):
        pass


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


class Temperature:
    def __init__(self, sensors):
        self.sensors = sensors

    def get_cpu_temperature_sensors(self):
        sensors_list = []
        if "Temperature" in str(self.sensors.keys()):
            for sensor in self.sensors["Temperature"]:
                if 'cpu' in str(sensor.Hardware.HardwareType).lower():
                    sensors_list.append(sensor)
        return sensors_list

    def get_gpu_temperature(self):
        sensors_list = []
        if "Temperature" in str(self.sensors.keys()):
            for sensor in self.sensors["Temperature"]:
                if 'gpu' in str(sensor.Hardware.HardwareType).lower():
                    sensors_list.append(sensor)
        return sensors_list

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
