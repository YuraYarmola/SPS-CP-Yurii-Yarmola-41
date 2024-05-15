import flet as ft


def get_usage_chart():
    usage_chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    # ft.LineChartDataPoint(0, 0),
                ],
                stroke_width=1,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
            )
        ],
        border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=0.5
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=0.5
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Text("0%", size=10, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=20,
                    label=ft.Text("20%", size=10, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=40,
                    label=ft.Text("40%", size=10, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=60,
                    label=ft.Text("60%", size=10, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=80,
                    label=ft.Text("80%", size=10, weight=ft.FontWeight.BOLD),
                ),
                ft.ChartAxisLabel(
                    value=100,
                    label=ft.Text("100%", size=10, weight=ft.FontWeight.BOLD),
                ),

            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Container(
                        ft.Text(
                            "0",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=30,
                    label=ft.Container(
                        ft.Text(
                            "30",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=60,
                    label=ft.Container(
                        ft.Text(
                            "60",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=100,
        min_x=0,
        max_x=60,
        expand=False,
        width=700,
        height=100,
    )
    return usage_chart


def get_temp_chart():
    temp_chart = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    # ft.LineChartDataPoint(0, 0),
                ],
                stroke_width=1,
                color=ft.colors.CYAN,
                curved=True,
                stroke_cap_round=True,
            )
        ],
        border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
        horizontal_grid_lines=ft.ChartGridLines(
            interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=0.5
        ),
        vertical_grid_lines=ft.ChartGridLines(
            interval=10, color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE), width=0.5
        ),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Text("0", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_300),

                ),
                ft.ChartAxisLabel(
                    value=20,
                    label=ft.Text("20", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_300),
                ),
                ft.ChartAxisLabel(
                    value=40,
                    label=ft.Text("40", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_300),
                ),
                ft.ChartAxisLabel(
                    value=60,
                    label=ft.Text("60", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.YELLOW_300),
                ),
                ft.ChartAxisLabel(
                    value=80,
                    label=ft.Text("80", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.RED_300),
                ),
                ft.ChartAxisLabel(
                    value=100,
                    label=ft.Text("100", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.RED_500),
                ),
                ft.ChartAxisLabel(
                    value=120,
                    label=ft.Text("120", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.RED_900),
                ),

            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=0,
                    label=ft.Container(
                        ft.Text(
                            "0",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=30,
                    label=ft.Container(
                        ft.Text(
                            "30",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
                ft.ChartAxisLabel(
                    value=60,
                    label=ft.Container(
                        ft.Text(
                            "60",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE),
                        ),
                        margin=ft.margin.only(top=10),
                    ),
                ),
            ],
            labels_size=40,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=120,
        min_x=0,
        max_x=60,
        expand=False,
        width=700,
        height=260,
    )
    return temp_chart
