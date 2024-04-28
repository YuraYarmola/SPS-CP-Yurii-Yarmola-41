from functions import *
from charts import *
import flet as ft
import time

last_page_index = 0


def main(page: ft.Page):
    body = ft.Column([], alignment=ft.MainAxisAlignment.START, expand=True)

    def change_chart(chart, value):
        if len(chart.data_series[0].data_points) < 60:
            chart.data_series[0].data_points.append(ft.LineChartDataPoint(
                len(chart.data_series[0].data_points), value), )
        else:
            chart.data_series[0].data_points = []

    def render_usage(e):
        timer = time.time()
        first = True
        destination_label = e.control.destinations[e.control.selected_index].label
        ram_progress = get_usage_chart()
        cpu_progress = get_usage_chart()

        while True:
            if destination_label != e.control.destinations[e.control.selected_index].label:
                break
            if e.control.destinations[e.control.selected_index].label == "Usage":
                if time.time() - timer > 1 or first:
                    first = False
                    ram_usage = MemoryUsageMonitor.get_memory_usage_percentage()  # 75%
                    cpu_usage = CPUUsageMonitor().get_cpu_utilization()
                    change_chart(ram_progress, ram_usage)
                    change_chart(cpu_progress, cpu_usage)

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
                    cpu_label = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Text(f"Usage:", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.Text(
                                    f"{cpu_usage}%",
                                    color=ft.colors.BLUE_400,
                                )
                                ,
                            ]),
                            ft.Row([
                                ft.Text("Frequency: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                                ft.Text(
                                    f"{CPUUsageMonitor().get_cpu_frequency().current} GHz",
                                    color=ft.colors.BLUE_400,
                                ),

                            ])

                        ],
                            spacing=2,
                        ),
                        margin=ft.Margin(left=150, right=0, top=0, bottom=10),
                    )

                    disks = []
                    disks_information = DiskSpaceMonitor().get_all_disk_usage()
                    for index, disk in enumerate(disks_information.keys()):
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
                                        ft.Text("Memory Usage Information\n"),
                                        ft.Text("RAM Information"),
                                        ram_label,
                                        ram_progress,
                                        ft.Text("CPU Information"),
                                        cpu_label,
                                        cpu_progress,
                                        ft.Text("\nDisks Information:"),

                                    ] + disks
                    timer = time.time()
                    page.update()

            else:
                break

    def render_temp(e):
        timer = time.time()
        first = True
        destination_label = e.control.destinations[e.control.selected_index].label

        cpu_temperature_chart = get_temp_chart()
        gpu_temperature_chart = get_temp_chart()

        while True:
            if destination_label != e.control.destinations[e.control.selected_index].label:
                break
            if e.control.destinations[e.control.selected_index].label == "Temp":
                if time.time() - timer > 1 or first:
                    first = False

                    cpu_temperature = Temperature().get_cpu_temperature()
                    if cpu_temperature:
                        cpu_temperature = cpu_temperature
                    else:
                        cpu_temperature = 0

                    gpu_temperature = Temperature().get_gpu_temperature()
                    if gpu_temperature:
                        gpu_temperature = gpu_temperature
                    else:
                        gpu_temperature = 0

                    change_chart(cpu_temperature_chart, cpu_temperature)
                    change_chart(gpu_temperature_chart, gpu_temperature)

                    body.controls = [
                        ft.Text(f"CPU Temperature {cpu_temperature}C°\n"),
                        cpu_temperature_chart,
                        ft.Text(f"GPU Temperature {gpu_temperature}C°\n"),
                        gpu_temperature_chart,
                    ]
                    page.update()
                    timer = time.time()
            else:
                break

    def render_system_info(e=None):
        information = SystemInformation().get_basic_system_info()
        information_labels = ft.Column()

        for key, value in information.items():
            information_labels.controls.append(
                ft.Row(
                    [
                        ft.Text(f"{key}:", style=ft.TextStyle(weight=ft.FontWeight.BOLD), size=20),
                        ft.Text(f"{value}", size=20),
                    ]
                )
            )
        body.controls = [
            information_labels,
        ]
        page.update()

    def render_processes(e):
        destination_label = e.control.destinations[e.control.selected_index].label

        processes_table = ft.DataTable(
            width=700,
            bgcolor=ft.colors.GREEN_600,
            border=ft.border.all(1, ft.colors.BLUE_200),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(2, ft.colors.BLUE_200),
            horizontal_lines=ft.border.BorderSide(1, "green"),
            sort_column_index=2,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            divider_thickness=0,
            data_row_color=ft.colors.GREY_900,
            columns=[
                ft.DataColumn(
                    ft.Text("pid", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
                ft.DataColumn(
                    ft.Text("name", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
                ft.DataColumn(
                    ft.Text("cpu_percent", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
                ft.DataColumn(
                    ft.Text("memory", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
            ],

        )

        def change_sort_index(index):
            processes_table.sort_column_index = index
            processes_table.sort_ascending = not processes_table.sort_ascending

        body.controls = [
            ft.Column([processes_table], scroll=ft.ScrollMode.ALWAYS, height=650),
        ]
        while True:
            if destination_label != e.control.destinations[e.control.selected_index].label:
                break
            if e.control.destinations[e.control.selected_index].label == "Processes":

                processes = Processes().get_processes()

                sorted_processes = sorted(processes,
                                          key=lambda x: x[[y for y in x.keys()][processes_table.sort_column_index]],
                                          reverse=not processes_table.sort_ascending, )

                data_rows = []
                for process in sorted_processes:
                    data_rows.append(
                        ft.DataRow([ft.DataCell(ft.Text(process.get("pid"))),
                                    ft.DataCell(ft.Text(process.get("name"))),
                                    ft.DataCell(ft.Text(process.get("cpu_percent"))),
                                    ft.DataCell(ft.Text(process.get("memory")))])
                    )

                if processes:
                    processes_table.rows = data_rows

                page.update()

            else:
                break

    def render_network(e):
        destination_label = e.control.destinations[e.control.selected_index].label
        data = []
        body.controls = [
            ft.Column(data, scroll=ft.ScrollMode.ALWAYS, height=650),
        ]
        while True:
            if destination_label != e.control.destinations[e.control.selected_index].label:
                break
            if e.control.destinations[e.control.selected_index].label == "Network":
                informations = NetworkTrafficMonitor().get_network_usage()
                for information in informations:
                    for key, value in information.items():
                        data.append(
                            ft.Row(
                                [
                                    ft.Text(f"{key}:", style=ft.TextStyle(weight=ft.FontWeight.BOLD), size=20),
                                    ft.Text(f"  {value}", size=20),
                                ]
                            )
                        )

                page.update()
                data = []
            else:
                break

    def render_logs(e):
        destination_label = e.control.destinations[e.control.selected_index].label

        processes_table = ft.DataTable(
            width=1000,
            bgcolor=ft.colors.GREEN_600,
            border=ft.border.all(1, ft.colors.BLUE_200),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(2, ft.colors.BLUE_200),
            horizontal_lines=ft.border.BorderSide(1, "green"),
            sort_column_index=2,
            heading_row_color=ft.colors.BLACK12,
            heading_row_height=100,
            divider_thickness=0,
            data_row_color=ft.colors.GREY_900,
            data_row_min_height=100,
            data_row_max_height=300,
            columns=[
                ft.DataColumn(
                    ft.Text("Event ID", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
                ft.DataColumn(
                    ft.Text("Time", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
                ft.DataColumn(
                    ft.Text("Source Name", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
                ft.DataColumn(
                    ft.Text("Message", color=ft.colors.BLACK, size=20),
                    on_sort=lambda e: change_sort_index(e.column_index),
                ),
            ],

        )

        def change_sort_index(index):
            processes_table.sort_column_index = index
            processes_table.sort_ascending = not processes_table.sort_ascending
            update_logs_DataRow(max_logs=int(dd_max.value), value=dd.value)

        def dropdown_changed(e):
            dd.value = dd.value
            update_logs_DataRow(value=dd.value)
            page.update()

        def dropdown_max_changed(e):
            dd_max.value = dd_max.value
            update_logs_DataRow(max_logs=int(dd_max.value))
            page.update()

        dd = ft.Dropdown(
            width=150,
            value='System',
            options=[
                ft.dropdown.Option("System"),
                ft.dropdown.Option("Application"),
                ft.dropdown.Option("Security"),
                ft.dropdown.Option("Setup"),
                ft.dropdown.Option("Forwarded Events"),
            ],
            on_change=dropdown_changed,
        )

        dd_max = ft.Dropdown(
            width=100,
            value="50",
            options=[
                ft.dropdown.Option("50"),
                ft.dropdown.Option("100"),
                ft.dropdown.Option("200"),
                ft.dropdown.Option("500"),
                ft.dropdown.Option("1000"),
            ],
            on_change=dropdown_max_changed,
        )

        body.controls = [
            ft.Row([dd, ft.Text("     "), dd_max]),
            ft.Column([processes_table], scroll=ft.ScrollMode.ALWAYS, height=650),
        ]

        def update_logs_DataRow(value="System", max_logs=50):

            processes = SystemInformation().get_event_logs(total_logs=max_logs, logtype=value)

            sorted_processes = sorted(processes,
                                      key=lambda x: x[
                                          [y for y in x.keys()]
                                          [processes_table.sort_column_index]
                                      ],
                                      reverse=not processes_table.sort_ascending, )

            data_rows = []
            for process in sorted_processes:
                data_rows.append(
                    ft.DataRow([ft.DataCell(ft.Text(process.get("Event ID"))),
                                ft.DataCell(ft.Text(process.get("Time"))),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(process.get("Source Name"), text_align=ft.TextAlign.JUSTIFY),
                                        width=200),
                                ),
                                ft.DataCell(
                                    ft.Container(
                                        content=ft.Text(process.get("Message"), text_align=ft.TextAlign.JUSTIFY),
                                        width=250)

                                )])
                )

            if processes:
                processes_table.rows = data_rows

            page.update()

        update_logs_DataRow()

    def change_body(e):
        global last_page_index
        destination_label = e.control.destinations[e.control.selected_index].label
        if last_page_index != e.control.selected_index:
            last_page_index = e.control.selected_index
            if destination_label == 'Usage':
                render_usage(e)
            elif destination_label == "Temp":
                render_temp(e)
            elif destination_label == "Info":
                render_system_info(e)
            elif destination_label == "Processes":
                render_processes(e)
            elif destination_label == "Network":
                render_network(e)
            elif destination_label == "System journal":
                render_logs(e)
            else:
                body.controls = [ft.Column([ft.Text(f"{destination_label}")])]
                page.update()

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
                icon=ft.icons.DATA_USAGE,
                label="Usage",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.THERMOSTAT,
                label="Temp",
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.MONITOR,
                label="Processes"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.NETWORK_WIFI,
                label="Network"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LIBRARY_BOOKS,
                label="System journal"
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
    render_system_info()


if __name__ == "__main__":
    ft.app(target=main)
