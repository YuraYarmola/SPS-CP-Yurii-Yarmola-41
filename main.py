import wmi

from functions import *
from charts import *
import flet as ft
import time


def main(page: ft.Page):
    body = ft.Column([ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True)

    def change_body(e):
        index = e.control.selected_index
        timer = time.time()
        first = True
        destination_label = e.control.destinations[index].label
        print(destination_label)
        run = True
        ram_progress = get_usage_chart()
        while run:
            if e.control.destinations[e.control.selected_index].label == "Storage":
                if time.time() - timer > 1 or first:
                    first = False
                    ram_usage = MemoryUsageMonitor.get_memory_usage_percentage()  # 75%
                    if len(ram_progress.data_series[0].data_points) < 60:
                        ram_progress.data_series[0].data_points.append(ft.LineChartDataPoint(
                            len(ram_progress.data_series[0].data_points), ram_usage), )
                    else:
                        ram_progress.data_series[0].data_points = []
                    used_memory = round(MemoryUsageMonitor.get_used_memory() / 1024 ** 3, 2)
                    total_memory = round(MemoryUsageMonitor.get_total_memory() / 1024 ** 3, 2)
                    ram_label = ft.Container(
                        content=ft.Row([
                            ft.Text(f"Usage: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                            ft.Text(
                                f"{used_memory}/"
                                f"{total_memory} GB"
                                f" ({MemoryUsageMonitor.get_memory_usage_percentage()}%)"
                                ,
                                color=ft.colors.BLUE_400,
                            )

                        ],
                            spacing=2,
                        ),
                        margin=ft.Margin(left=150, right=0, top=0, bottom=10),
                    )

                    disks = []
                    disks_information = DiskSpaceMonitor().get_all_disk_usage()
                    for disk in disks_information.keys():
                        disks.append(
                            ft.Container(content=ft.Column([
                                ft.Row(
                                    [
                                        ft.Text(f"{disk}", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                        ft.Text(f"{round(disks_information[disk]['used'] / 1024 ** 3, 2)} GB"
                                                f"/{round(disks_information[disk]['total'] / 1024 ** 3, 2)} GB",
                                                color=ft.colors.BLUE_400),
                                        ft.Text(f"({round(disks_information[disk]['percent'], 2)}%)",
                                                color=ft.colors.BLUE_400)
                                    ]
                                ),
                                ft.ProgressBar(value=disks_information[disk]['percent'] / 100, width=400, height=20),

                            ]
                            ),
                                margin=ft.Margin(left=0, right=0, top=0, bottom=20),
                        ),

                        )

                    body.controls = [
                                        ft.Text("Memory Information\n"),
                                        ft.Text("RAM Information"),
                                        ram_label,
                                        ft.Row(
                                            [
                                                # ft.Column([ram_label,
                                                #            ],
                                                #           width=250),
                                                ft.Column([ram_progress,
                                                           ])
                                            ], spacing=10),
                                        ft.Text("\nDisks Information:"),

                                    ] + disks
                    timer = time.time()
                    page.update()
            else:
                body.controls = [ft.Text(f"Selected Page: {destination_label}")]
                page.update()
                break

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        extended=True,
        min_width=100,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.INFO,
                label="Info"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SD_STORAGE,
                label="Storage",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.THERMOSTAT,
                label="Temp",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.NETWORK_WIFI,
                label="Network"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LIBRARY_BOOKS,
                label="System journal"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.NOTIFICATIONS,
                label='Notifications'
            ),
        ],
        on_change=change_body,
    )

    layout = ft.Row(
        [
            rail,
            ft.VerticalDivider(width=1),
            body
        ],
        expand=True,
    )

    page.add(layout)


if __name__ == "__main__":
    ft.app(target=main)

# if __name__ == "__main__":
# system_monitor = SystemMonitor()
# system_monitor.start_monitoring()
#
# print(Sensor().sensors)
# sensors = Sensor()
# sensor = Temperature(sensors.sensors).get_gpu_temperature()[0]
# while True:
#     sensors.handle.Hardware[0].Update()
#     print(sensor.Value)
# cpu_monitor = CPUUsageMonitor()
# memory_monitor = MemoryUsageMonitor()
#
# e.g. clr.AddReference(r'OpenHardwareMonitor/OpenHardwareMonitorLib'), without .dll
# import clr  # package pythonnet, not clr
# import shutil
#
# # openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
# openhardwaremonitor_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer',
#                                'Heatmaster', 'HDD']
# cputhermometer_hwtypes = ['Mainboard', 'SuperIO', 'CPU', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']
# openhardwaremonitor_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level',
#                                    'Factor', 'Power', 'Data', 'SmallData']
# cputhermometer_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level']
#
#
# def initialize_openhardwaremonitor():
#     file = r'D:\LPNU\SEMESTR 6\SPZ\KURSOVA\SystemMonitor\SPS-CP-Yurii-Yarmola-41\OpenHardwareMonitorLib.dll'
#     clr.AddReference(file)
#
#     from OpenHardwareMonitor import Hardware
#
#     handle = Hardware.Computer()
#     handle.MainboardEnabled = True
#     handle.CPUEnabled = True
#     handle.RAMEnabled = True
#     handle.GPUEnabled = True
#     handle.HDDEnabled = True
#     handle.Open()
#     return handle
#
#
# def fetch_stats(handle):
#     for i in handle.Hardware:
#         i.Update()
#         for sensor in i.Sensors:
#             parse_sensor(sensor)
#             print(sensor.Hardware.Name)
#         for j in i.SubHardware:
#             j.Update()
#             for subsensor in j.Sensors:
#                 parse_sensor(subsensor)
#
#
#
# def parse_sensor(sensor):
#     if sensor.Value is not None:
#         if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
#             sensortypes = openhardwaremonitor_sensortypes
#             hardwaretypes = openhardwaremonitor_hwtypes
#             hardwaretypes = openhardwaremonitor_hwtypes
#         else:
#             return
#
#         if 'Temperature' in str(sensor.SensorType):
#             print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" % (
#             hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name,
#             sensor.Value))
#
#
# if __name__ == "__main__":
#     HardwareHandle = initialize_openhardwaremonitor()
#     fetch_stats(HardwareHandle)
# while True:
#     cpu_usage = cpu_monitor.get_cpu_usage()
#     memory_usage = memory_monitor.get_memory_usage()
#
#     cpu_monitor.notify_if_threshold_exceeded()
#     memory_monitor.notify_if_threshold_exceeded()
#
# system_monitor.stop_monitoring()
