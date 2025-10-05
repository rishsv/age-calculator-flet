import flet as ft
from datetime import datetime
from dateutil.relativedelta import relativedelta
import threading

def days_until_next_birthday(birth_date):
    today = datetime.now().date()
    this_year = today.year
    month = birth_date.month
    day = birth_date.day
    try:
        next_birthday = datetime(this_year, month, day).date()
    except ValueError:
        # Handle Feb 29 on non-leap years: next leap year
        next_year = this_year + 1
        while True:
            if (month, day) == (2, 29) and not (
                next_year % 4 == 0 and (next_year % 100 != 0 or next_year % 400 == 0)
            ):
                next_year += 1
            else:
                break
        next_birthday = datetime(next_year, month, day).date()

    if next_birthday < today:
        try:
            next_birthday = datetime(this_year + 1, month, day).date()
        except ValueError:
            next_year = this_year + 1
            while True:
                if (month, day) == (2, 29) and not (
                    next_year % 4 == 0 and (next_year % 100 != 0 or next_year % 400 == 0)
                ):
                    next_year += 1
                else:
                    break
            next_birthday = datetime(next_year, month, day).date()

    days_left = (next_birthday - today).days
    return days_left

def main(page: ft.Page):
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.DEEP_PURPLE,
        use_material3=True
    )
    page.title = "Age Calculator"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False

    selected_date = datetime.now()
    age_years = ft.Text("--", size=48, weight=ft.FontWeight.BOLD)
    age_months = ft.Text("--", size=32)
    age_days = ft.Text("--", size=32)
    birthday_countdown = ft.Text("--", size=24, color=ft.Colors.DEEP_PURPLE)
    # Celebration icon row, initially hidden
    celebration_container = ft.Row(
        controls=[
            ft.Icon(ft.Icons.CELEBRATION, size=40, color=ft.Colors.ORANGE),
            ft.Icon(ft.Icons.CELEBRATION, size=40, color=ft.Colors.PINK),
            ft.Icon(ft.Icons.CELEBRATION, size=40, color=ft.Colors.BLUE),
        ],
        visible=False,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10,
    )

    def update_age(birth_date):
        today = datetime.now()
        delta = relativedelta(today, birth_date)
        age_years.value = f"{delta.years}"
        age_months.value = f"{delta.months} months"
        age_days.value = f"{delta.days} days"
        days_left = days_until_next_birthday(birth_date)
        if days_left == 0:
            birthday_countdown.value = "0 days — Happy Birthday! 🎉"
            birthday_countdown.color = ft.Colors.ORANGE
            celebration_container.visible = True
            page.update()
            # Hide after 5 seconds
            def hide_celebration():
                celebration_container.visible = False
                page.update()
            threading.Timer(5.0, hide_celebration).start()
        else:
            birthday_countdown.value = f"{days_left} days"
            birthday_countdown.color = ft.Colors.DEEP_PURPLE
            celebration_container.visible = False

        page.update()

    def handle_date_pick(e):
        nonlocal selected_date
        if date_picker.value:
            selected_date = datetime(
                date_picker.value.year,
                date_picker.value.month,
                date_picker.value.day,
            )
            selected_date_display.value = selected_date.strftime("%B %d, %Y")
            date_picker.open = False
            update_age(selected_date)
        page.update()

    date_picker = ft.DatePicker(on_change=handle_date_pick)
    page.overlay.append(date_picker)

    def open_date_picker(e):
        date_picker.open = True
        page.update()

    selected_date_display = ft.Text(
        "Select your birth date", 
        size=18,
        weight=ft.FontWeight.W_500
    )

    age_display = ft.Card(
        elevation=8,
        content=ft.Container(
            width=300,
            padding=30,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text("AGE", size=18),
                    age_years,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    age_months,
                    age_days,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text("Days until next birthday:", size=16),
                    birthday_countdown,
                ]
            )
        )
    )

    github_button = ft.FloatingActionButton(
        icon=ft.Icons.CODE,
        shape=ft.CircleBorder(),
        tooltip="View GitHub Repository",
        mini=True,
        on_click=lambda _: page.launch_url("https://github.com/virendracarpenter")
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40,
            controls=[
                ft.Icon(ft.Icons.CAKE, size=40),
                selected_date_display,
                age_display,
                celebration_container,  # Add this to main layout!
                ft.ElevatedButton(
                    "Select Birth Date",
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=open_date_picker,
                ),
            ]
        ),
        ft.Container(
            alignment=ft.alignment.bottom_center,
            margin=ft.margin.only(bottom=50),
            content=github_button
        )
    )

ft.app(target=main)
