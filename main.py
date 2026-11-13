from bakery import assert_equal
from drafter import *
from dataclasses import dataclass, field


PROGRAM_NAME = "[Temporary Program Name]"

set_website_title(PROGRAM_NAME)
set_site_information(
    author="Nathaniel White",
    description="Manage custom calendars with Drafter.",
    sources="Drafter docs, some LLM interaction, Forgotten Realms campaign setting.",
    planning=[],
    links=["https://github.com/nwhite86/drafter-calendar"]
)
hide_debug_information()
set_website_framed(False)










#####################################################################################################################
# Here is the contents of custom_calendar.py because when I try to have them as separate files in GitHub, it crashes.
# And I don't have time to figure that out.
####################################################################################################################

@dataclass
class Time:
    """A time of day, with hours and minutes
    fields::
        hour: int - between 0 and [length of day] in hours.
        minute: int - between 0 and [length of hour] in minutes
    """
    hour: int = 0
    minute: int = 0

    def print_time(self):
        """
        Prints the time in hours and minutes.

        Displays the hour followed by the minute, with the minute
        padded to two digits when necessary.

        Returns:
            None
        """
        print(f"{self.hour}:{self.minute:02d}")


@dataclass
class Event:
    """
    Represents an event occurring on a particular calendar date.

    Attributes:
        day (int): The day of the month on which the event occurs.
        month (int): The index of the month in which the event occurs.
        start_time (Time): The time at which the event begins.
        end_time (Time): The time at which the event ends.
    """
    day: int
    month: int
    start_time: Time
    end_time: Time


@dataclass
class Year:
    """
    Represents a customizable calendar year.

    Stores information about the structure, naming conventions,
    and calendar rules of a year. Supports customizable month
    lengths, weekday lengths, leap-year rules, floating days,
    and calendar events.

    Attributes:
        year_number (int): The numerical identifier of the year. (Current year)
        days_per_year (int): The number of regular days in the year,
            excluding floating days.
            1-indexed
        months_per_year (int): The number of months in the year.
            0-indexed

        has_leap_day (bool): Whether the calendar supports leap days.
        has_floating_leap_day (bool): Whether leap days are treated
            as floating days.
        years_per_leap (int): The number of years between leap years.
        leap_day (int): The position of the leap day in the year.
        has_centry_rule (bool): Whether the century leap-year rule
            is applied.
        years_per_century (int): The number of years in a century.

        days_per_week (int): The number of days in a week.
        days_per_month (list[int]): The number of days in each month.

        floating_days (dict): A dictionary containing floating days,
            indexed by their position relative to a month and day.
        events (list[Event]): A collection of events belonging to
            the calendar year.

        year_name (str): The custom name of the year.
        month_names (list[str]): The names of the months.
        weekday_names (list[str]): The names of the weekdays.

    Notes:
        The calendar assumes that the first day of year 1 is the
        first day of the week. Weekday calculations are based on
        this assumption.
    """

    # TODO:
    # Floating days implementation
    # events implementation

    year_number: int = 2026

    # days_per_year can not include floating days
    days_per_year: int = 365
    months_per_year: int = 12

    # Leap Day Rules
    has_leap_day: bool = True
    has_floating_leap_day: bool = False
    #
    years_per_leap: int = 4
    leap_day: int = 60
    #
    # The century rule is a funny little rule that says that leap years don't apply on
    # years that are multiples of 100, unless they're also multiples of 400
    has_centry_rule: bool = False
    years_per_century: int = 100
    #

    # Important day of week note: This calander program assumes that the first day of year 1 is the first day of the week.
    # This is used to calculate the day of the week.

    # For the defualt settings, 1 is a Monday.

    days_per_week: int = 7
    days_per_month: list[int] = field(default_factory=lambda: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

    floating_days: dict = field(default_factory=dict)
    """
    floating_days format:
    {
        tuple: str
            (the month that the floating day is before / within, the day that the floating day before): "Name" 
    }
    """

    events: list[Event] = field(default_factory=lambda: [])

    # Custom Names
    year_name: str = "[DEFAULT YEAR NAME]"
    month_names: list[str] = field(
        default_factory=lambda: ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                                 "October", "November", "December"])
    weekday_names: list[str] = field(
        default_factory=lambda: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    # Custom Name Functions
    def get_weekday_name(self, weekday: int) -> str:
        """
        Retrieves the name of a weekday using its numerical index.

        Args:
            weekday (int): The zero-indexed position of the weekday.

        Returns:
            str: The name of the specified weekday.
        """
        return self.weekday_names[weekday]

    def get_month_name(self, month: int) -> str:
        """
        Retrieves the name of a month using its numerical index.

        Args:
            month (int): The zero-indexed position of the month.

        Returns:
            str: The name of the specified month.
        """
        return self.month_names[month]

    # Calander Logic Functions

    def get_weekday(self, month: int, day: int) -> int:
        """
        Calculates the weekday corresponding to a given date.

        Determines the weekday by accounting for the number of days
        in previous months, the starting weekday of the year, and
        any applicable leap-year adjustments.

        Args:
            month (int): The zero-indexed month of the date.
            day (int): The zero-indexed day within the month.

        Returns:
            int: The zero-indexed weekday corresponding to the date.

        Notes:
            The first day of year 1 is assumed to be the first day
            of the week. Leap-year and century rules are applied
            according to the calendar's configuration.
        """
        first_weekday_of_year = ((self.year_number - 1) * self.days_per_year) % self.days_per_week
        day_of_year = sum(self.days_per_month[:month]) + day
        # Step 1: Account for leap day in current year

        if self.has_leap_day and not self.has_floating_leap_day:
            # If it's a leap year
            is_leap_year = self.year_number % self.years_per_leap == 0
            # If the century rule applies and it's not a century leap year, update is_leap_year
            if self.has_centry_rule and is_leap_year:
                # If it is NOT a century leap year (the year is divisible by 400)
                if self.year_number % (self.years_per_leap * self.years_per_century) != 0:
                    is_leap_year = False
            if is_leap_year and day_of_year > self.leap_day:
                day_of_year += 1

            # Step 2: Find the offset in they day of the week from previous leap years
            leap_year_offset = (self.year_number - 1) // self.years_per_leap
            # If there's a centry rule, remove leap days for every year affected
            if self.has_centry_rule:
                leap_year_offset -= (self.year_number - 1) // self.years_per_century - (self.year_number - 1) // (
                            self.years_per_leap * self.years_per_century)

            day_of_year += leap_year_offset
        # Step 3: Use day_of_year + leap_year_offset % days_per_week to get the current day of the week
        # I need this -1 because days_per_week is 1 indexed, but everything else has been 0 indexed
        #                                                                           \/
        day_of_week = (day_of_year + first_weekday_of_year) % (self.days_per_week)

        return day_of_week

    # Displaying Calander
    def print_month(self, month: int):
        """
        Prints a formatted calendar representation of a month.

        Displays the month name, year number, weekday headers,
        and numbered dates. Dates are aligned with their
        corresponding weekdays using leading whitespace.

        Args:
            month (int): The zero-indexed month to display.

        Returns:
            None

        Notes:
            Floating days are not currently included in the output.
        """
        # todo:
        #  Figure out how to display floating months

        # Step 1: Printing the month
        # Print Title
        print(f"\t\t{self.get_month_name(month)}, {self.year_number}")

        # Print weekdays
        for weekday in self.weekday_names:
            print(weekday[:3], "\t", sep="", end="")
        print()

        dates = [i + 1 for i in range(self.days_per_month[month])]
        whitespace = ["-"] * self.get_weekday(month=month, day=0)

        dates = whitespace + dates

        for i, date in enumerate(dates):
            print(date, "\t", sep="", end="")
            if (i + 1) % self.days_per_week == 0:
                print()
        print()

        # Step 2: Printing any floating days

    def get_day_string(self, month: int, day: int) -> str:
        """
        Generates a formatted string describing a calendar date.

        Example: 'Sunday, May 3'

        Combines the weekday name, month name, and day number
        into a human-readable date representation.

        Args:
            month (int): The zero-indexed month of the date.
            day (int): The one-indexed day of the month.

        Returns:
            str: A formatted date string containing the weekday,
            month, and day.
        """
        return f"{self.get_weekday_name(self.get_weekday(month, day) - 1)}, {self.get_month_name(month)} {day} \n"


fd = {
    (10, 11): "Nathaniel's Favorite Day"
}
# test_year = Year(has_centry_rule=True, floating_days=fd)

# print(test_year)

# test_year.print_month(10)

forgotten_realms_months = [
    "Hammer",
    "Alturiak",
    "Ches",
    "Tarsakh",
    "Mirtul",
    "Kythorn",
    "Flamerule",
    "Eleasis",
    "Eleint",
    "Marpenoth",
    "Uktar",
    "Nightal",
]

forgotten_reams_year = Year(
    year_number=1492,
    days_per_year=360,
    months_per_year=12,

    has_leap_day=False,

    days_per_week=10,
    days_per_month=([30] * 12),

    year_name="Year of the Seven Ships Sailing",
    month_names=forgotten_realms_months,
    weekday_names=["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
)

#############################################################
# Unit tests:

# ==========================================
# Testing Time
# ==========================================

assert_equal(Time(0, 0), Time(0, 0))
assert_equal(Time(12, 30), Time(12, 30))
assert_equal(Time(23, 59), Time(23, 59))

# ==========================================
# Testing Event
# ==========================================

assert_equal(Event(1, 0, Time(9, 0), Time(10, 0)),
             Event(1, 0, Time(9, 0), Time(10, 0)))

assert_equal(Event(5, 2, Time(12, 0), Time(13, 0)).day, 5)
assert_equal(Event(5, 2, Time(12, 0), Time(13, 0)).month, 2)

# ==========================================
# Testing Year Initialization
# ==========================================

assert_equal(forgotten_reams_year.year_number, 1492)
assert_equal(forgotten_reams_year.days_per_year, 360)
assert_equal(forgotten_reams_year.months_per_year, 12)

# ==========================================
# Testing get_weekday_name()
# ==========================================

assert_equal(forgotten_reams_year.get_weekday_name(0), "1st")
assert_equal(forgotten_reams_year.get_weekday_name(4), "5th")
assert_equal(forgotten_reams_year.get_weekday_name(9), "10th")

# ==========================================
# Testing get_month_name()
# ==========================================

assert_equal(forgotten_reams_year.get_month_name(0), "Hammer")
assert_equal(forgotten_reams_year.get_month_name(5), "Kythorn")
assert_equal(forgotten_reams_year.get_month_name(11), "Nightal")

# ==========================================
# Testing get_weekday()
# ==========================================

assert_equal(forgotten_reams_year.get_weekday(0, 0), 0)
assert_equal(forgotten_reams_year.get_weekday(0, 1), 1)
assert_equal(forgotten_reams_year.get_weekday(1, 0), 0)
assert_equal(forgotten_reams_year.get_weekday(11, 29), 9)

# ==========================================
# Testing get_day_string()
# ==========================================

assert_equal(forgotten_reams_year.get_day_string(0, 1), "1st, Hammer 1 \n")

assert_equal(forgotten_reams_year.get_day_string(0, 2), "2nd, Hammer 2 \n")

assert_equal(forgotten_reams_year.get_day_string(1, 1), "1st, Alturiak 1 \n")

# ==========================================
# Testing print_month()
# ==========================================

# These tests check that the method executes without errors.
# Visual output can be inspected in the console.

forgotten_reams_year.print_month(0)
forgotten_reams_year.print_month(5)
forgotten_reams_year.print_month(11)

print("Testing complete!")


#####################################################################################################################
# Here is the contents of custom_calendar.py because when I try to have them as separate files in GitHub, it crashes.
# And I don't have time to figure that out.
####################################################################################################################




















# Global Constants
# todo: create dataclass to store time information.
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60

# Helper Functions

def display_month_drafter(year: Year, month: int) -> list:
    """
    Generates the Drafter content used to display a calendar month.

    Creates a calendar table containing weekday headers and individual
    buttons for each day. Each day button navigates to the day_info
    route with the corresponding date as an argument. Leading empty
    spaces are added to align the dates with their correct weekdays.

    Args:
        year (Year): The Year object containing calendar information.
        month (int): The index of the month to display.

    Returns:
        list: A list of Drafter content elements representing the
        calendar month.
    """
    # Useful debug in the console to know what it's supposed to look like
    year.print_month(month)

    # Create empty content list
    content = []
    # This will become the actual table content
    table_content = []
    # This will become the Table's rows argument
    table_rows = []

    # Add title
    content.append(Header(year.get_month_name(month), 3))

    # Add weekday titles
    for weekday in year.weekday_names:
        table_rows.append(weekday[:3])

    dates = [i + 1 for i in range(year.days_per_month[month])]
    whitespace = ["-"] * year.get_weekday(month=month, day=0)

    dates = whitespace + dates

    row = []
    for i, date in enumerate(dates):
        if isinstance(date, int):
            row.append(Button(str(date), "day_info", [Argument("date", date)]))
        else:
            row.append("")

        # If the week ended, wrap around
        if (i + 1) % year.days_per_week == 0:
            table_content.append(row)
            row = []

    content.append(Table(table_content, table_rows))

    return content

def display_month_timeline(year: Year, displayed_month: int):
    """
    Generates navigation controls for moving between calendar months.

    Creates a label displaying the current month and its position
    within the year, along with buttons for navigating to the
    previous or next month when those months exist.

    Args:
        year (Year): The Year object containing calendar information.
        displayed_month (int): The index of the currently displayed month.

    Returns:
        list: A list of Drafter content elements containing the
        month label and navigation controls.
    """
    content = []

    # If there is room to go left, add a button to go left
    if displayed_month != 0:
        content.append(
            Button("<", "increment_month", [Argument("amount", -1)]))
    else:
        content.append("[ < ]")
    # Add a label
    # TODO: Update the fstring for dynamic length
    # Currently it's hardcoded for a length of 2 digits. What if there are 100+ months?
    content.append(f"Change Month ({displayed_month + 1:02d}/{year.months_per_year})")
    # If there is room to go right, add a button to go right
    if displayed_month != year.months_per_year - 1:
        content.append(
            Button(">", "increment_month", [Argument("amount", 1)]))
    else:
        content.append("[ > ]")

    return content

# Drafter routes

@dataclass
class State:
    year: Year
    #current_time: Time
    displayed_month: int


@route
def index(state: State) -> Page:
    """
    Displays the program's landing page.

    Provides navigation options for defining a new calendar or
    loading an existing calendar.

    Args:
        state (State): The current application state.

    Returns:
        Page: The landing page containing the program title and
        calendar navigation buttons.
    """
    return Page(state, [
        "Welcome to ", PROGRAM_NAME, "\n",
        Button("Define Calender", "define_calender"),
        Button("Load Calender", "load_calender")

    ])



@route
def define_calender(state: State) -> Page:
    """
    Displays the calendar creation page.

    This is where users will define a custom calendar system.

    Currently serves as a placeholder for the future calendar
    creation functionality and provides navigation to the main
    calendar page.

    Args:
        state (State): The current application state.

    Returns:
        Page: The calendar creation page.
    """
    return Page(state, [
        "Define New Calender",
        "This is a placeholder until the backend logic is finished",
        Button("Continue to main calender page", "main_page")
    ])


@route
def load_calender(state: State) -> Page:
    """
    Load a preexising calendar.

    Currently serves as a placeholder for the future functionality
    to load an existing calendar and provides navigation to the
    main calendar page.

    Args:
        state (State): The current application state.

    Returns:
        Page: The calendar loading page.
    """
    return Page(state, [
        "This is a placeholder until the backend logic is finished",
        Button("Continue to main calender page", "main_page")
    ])

@route
def day_info(state: State, date: int) -> Page:
    """
    Displays information about a selected calendar day.

    Retrieves the selected day's date string from the current Year
    object and provides an option to add an event to that day.

    Args:
        state (State): The current application state.
        date (int): The day of the month to display.

    Returns:
        Page: A page displaying the selected day's information
        and available actions.
    """
    return Page(state, [
        "DAY INFO\n",
        state.year.get_day_string(state.displayed_month, date),
        "This is a placeholder until the backend logic is finished",
        Button("Add event", "add_event", arguments=[Argument("date", date)]),
        Button("Return to main calender page", "main_page")
    ])

@route
def add_event(state: State, date: int) -> Page:
    """
    Displays the event creation form for a selected calendar day.

    Provides textboxes for entering an event name, start time,
    and end time. The entered information is submitted to the
    save_event route for validation and processing.

    Args:
        state (State): The current application state.
        date (int): The day of the month to which the event
        will be assigned.

    Returns:
        Page: A page containing the event creation form.
    """
    return Page(state, [
        "Event for",
        state.year.get_day_string(state.displayed_month, date), "\n",
        "Event Name: ",
        TextBox("event_name", ""),
        "\n",
        "Event Start Time:",
        TextBox("start_hour", "0", "number"),
        ":",
        TextBox("start_minute", "0", "number"),
        "\n",
        "Event End Time:",
        TextBox("end_hour", "0", "number"),
        ":",
        TextBox("end_minute", "0", "number"),

        "\n",
        Button("Save Event", "save_event", arguments=[Argument("date", date)]),
    ])

@route
def save_event(state: State, date: int, event_name: str,
               start_hour: float, start_minute: float,
               end_hour: float, end_minute: float) -> Page:
    """
    Validates and saves a new calendar event.

    Checks that the provided start and end times contain integer
    values and fall within the valid hours and minutes of a day.
    If validation succeeds, creates a new Event object, adds it
    to the current year's event list, and returns to the selected
    day's information page.

    If validation fails, displays an error message and provides
    an option to return to the event creation form.

    Args:
        state (State): The current application state.
        date (int): The day of the month to which the event
        will be assigned.
        event_name (str): The name of the event.
        start_hour (float): The event's starting hour.
        start_minute (float): The event's starting minute.
        end_hour (float): The event's ending hour.
        end_minute (float): The event's ending minute.

    Returns:
        Page: Either the selected day's information page if the
        event is successfully saved, or an error page if validation
        fails.
    """    # Step 1: Validate the user's input
    # Are the hours and minutes integers?
    try:
        start_hour = int(start_hour)
        start_minute = int(start_minute)

        end_hour = int(end_hour)
        end_minute = int(end_minute)
    except:
        return Page(state, content=[
            "Your times must be integers.", "\n",
            Button("Ok", "add_event", arguments=[Argument("date", date)])
        ])
    # Are the hours and minutes within the day?
    if not ( (HOURS_PER_DAY > start_hour >= 0) and (MINUTES_PER_HOUR > start_minute >= 0)
         and (HOURS_PER_DAY > end_hour >= 0) and (MINUTES_PER_HOUR > end_minute >= 0)):
        return Page(state, content=[
            "Your times must be within the hours and minutes per day.", "\n",
            Button("Ok", "add_event", arguments=[Argument("date", date)])
        ])

    # Step 2: Create new event
    start_time = Time(
        hour = start_hour,
        minute = start_minute,
    )

    end_time = Time(
        hour = end_hour,
        minute = end_minute
    )

    new_event = Event(
        day = date,
        month = state.displayed_month,
        start_time = start_time,
        end_time = end_time
    )

    # Step 3: Update State and return
    state.year.events.append(new_event)

    return day_info(state, date)


@route
def increment_month(state: State, amount: int) -> Page:
    """
    Changes the currently displayed calendar month.

    Updates the displayed_month attribute of the application state
    by the specified amount and returns to the main calendar page.

    Args:
        state (State): The current application state.
        amount (int): The number of months to move forward or
        backward. Positive values move forward, while negative
        values move backward.

    Returns:
        Page: The updated main calendar page.
    """
    #todo: Make sure that the displayed month is within bounds. Perhaps just wrap around.
    state.displayed_month += amount
    return main_page(state)

@route
def main_page(state: State) -> Page:
    """
    Displays the main calendar interface.

    Generates the calendar page header using the current year's
    information, displays the currently selected month, and adds
    navigation controls for changing months.

    Args:
        state (State): The current application state.

    Returns:
        Page: The main calendar page containing the year header,
        monthly calendar, and month navigation controls.
    """

    content = [
        "This is a placeholder until the backend logic is finished\n",
    ]

    header = str(state.year.year_number)
    if state.year.year_name:
        header += (", " + state.year.year_name)

    content.append(Header(header, 2)),

    # Add visual calendar
    content += display_month_drafter(state.year, state.displayed_month)

    content += display_month_timeline(state.year, state.displayed_month)

    return Page(state, content)

forgotten_realms_months = [
    "Hammer",
    "Alturiak",
    "Ches",
    "Tarsakh",
    "Mirtul",
    "Kythorn",
    "Flamerule",
    "Eleasis",
    "Eleint",
    "Marpenoth",
    "Uktar",
    "Nightal",
]

forgotten_reams_year = Year(
    year_number=1492,
    days_per_year=360,
    months_per_year=12,

    has_leap_day=False,

    days_per_week=10,
    days_per_month=([30] * 12),

    year_name="Year of the Seven Ships Sailing",
    month_names=forgotten_realms_months,
    weekday_names=["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
)


display_month_drafter(
    year=forgotten_reams_year, month=2)


###################################################################
# Unit Tests

def make_test_year(year_name="Test Year"):
    return Year(
        year_number=2024,
        days_per_year=360,
        months_per_year=12,
        has_leap_day=False,
        days_per_week=10,
        days_per_month=[30] * 12,
        year_name=year_name,
        month_names=[
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ],
        weekday_names=[
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday", "Eighth",
            "Ninth", "Tenth"
        ]
    )


def make_test_state(month=0, day=0):
    return State(
        year=make_test_year(),
        displayed_month=month
    )


# ==========================================
# display_month_drafter()
# ==========================================

year_test = make_test_year()
result = display_month_drafter(year_test, 0)

# Test 1: Correct month header
assert assert_equal(result[0], Header("January", 3))

# Test 2: Correct weekday headers
expected_headers = [
    "Mon", "Tue", "Wed", "Thu", "Fri",
    "Sat", "Sun", "Eig", "Nin", "Ten"
]
assert assert_equal(result[1].header, expected_headers)


# ==========================================
# display_month_timeline()
# ==========================================

year_test = make_test_year()

# Test 1: First month has no previous button
result = display_month_timeline(year_test, 0)

assert assert_equal(result[0], "[ < ]")
assert assert_equal(result[1], "Change Month (01/12)")

# Test 2: Middle month has both navigation buttons
result = display_month_timeline(year_test, 5)

assert assert_equal(
    result[0],
    Button("<", "increment_month", [Argument("amount", -1)])
)
assert assert_equal(
    result[2],
    Button(">", "increment_month", [Argument("amount", 1)])
)

# Test 3: Last month has no next button
result = display_month_timeline(year_test, 11)

assert assert_equal(result[1], "Change Month (12/12)")
assert assert_equal(result[2], "[ > ]")


# ==========================================
# index()
# ==========================================

state = make_test_state()
result = index(state)

# Test 1: Welcome message
assert assert_equal(result.content[0], "Welcome to ")

# Test 2: Define calendar button
assert assert_equal(
    result.content[3],
    Button("Define Calender", "define_calender")
)

# Test 3: Load calendar button
assert assert_equal(
    result.content[4],
    Button("Load Calender", "load_calender")
)


# ==========================================
# define_calender()
# ==========================================

state = make_test_state()
result = define_calender(state)

# Test 1: Correct page title
assert assert_equal(result.content[0], "Define New Calender")

# Test 2: Placeholder message
assert assert_equal(
    result.content[1],
    "This is a placeholder until the backend logic is finished"
)

# Test 3: Navigation button
assert assert_equal(
    result.content[2],
    Button("Continue to main calender page", "main_page")
)


# ==========================================
# load_calender()
# ==========================================

state = make_test_state()
result = load_calender(state)

# Test 1: Placeholder message
assert_equal(
    result.content[0],
    "This is a placeholder until the backend logic is finished"
)

# Test 2: Navigation button
assert_equal(
    result.content[1],
    Button("Continue to main calender page", "main_page")
)

# Test 3: State remains unchanged
assert_equal(result.state, state)


# ==========================================
# day_info()
# ==========================================

state = make_test_state()
result = day_info(state, 5)

# Test 1: Correct page title
assert_equal(result.content[0], "DAY INFO\n")

# Test 2: Correct date information
assert_equal(
    result.content[1],
    state.year.get_day_string(0, 5)
)

# Test 3: Add event button contains correct date
assert_equal(
    result.content[3],
    Button("Add event", "add_event",
           arguments=[Argument("date", 5)])
)


# ==========================================
# add_event()
# ==========================================

state = make_test_state()
result = add_event(state, 10)

# Test 1: Correct date displayed
assert_equal(
    result.content[1],
    state.year.get_day_string(0, 10)
)

# Test 2: Event name textbox
assert_equal(result.content[4], TextBox("event_name", ""))

# Test 3: Save button contains correct date
assert_equal(
    result.content[-1],
    Button("Save Event", "save_event",
           arguments=[Argument("date", 10)])
)


# ==========================================
# save_event()
# ==========================================

state = make_test_state()

# Test 1: Reject non-integer time input
result = save_event(
    state, 5, "Meeting",
    "abc", "30", "10", "30"
)

assert_equal(
    result.content[0],
    "Your times must be integers."
)
assert_equal(len(state.year.events), 0)


# Test 2: Reject invalid time ranges
state = make_test_state()

result = save_event(
    state, 5, "Meeting",
    "10", "60", "11", "30"
)

assert_equal(
    result.content[0],
    "Your times must be within the hours and minutes per day."
)
assert_equal(len(state.year.events), 0)


# Test 3: Successfully create an event
state = make_test_state()

result = save_event(
    state, 5, "Meeting",
    "9", "30", "10", "45"
)

expected_event = Event(
    day=5,
    month=0,
    start_time=Time(hour=9, minute=30),
    end_time=Time(hour=10, minute=45)
)

assert_equal(len(state.year.events), 1)
assert_equal(state.year.events[0], expected_event)
assert_equal(result.content[0], "DAY INFO\n")


# ==========================================
# increment_month()
# ==========================================

# Test 1: Increment month
state = make_test_state(month=0)
result = increment_month(state, 1)

assert_equal(state.displayed_month, 1)

# Test 2: Decrement month
state = make_test_state(month=5)
result = increment_month(state, -1)

assert_equal(state.displayed_month, 4)

# Test 3: Increment by zero
state = make_test_state(month=7)
result = increment_month(state, 0)

assert_equal(state.displayed_month, 7)


# ==========================================
# main_page()
# ==========================================

# Test 1: Year header with year name
state = make_test_state()
result = main_page(state)

assert_equal(
    result.content[1],
    Header("2024, Test Year", 2)
)

# Test 2: Year header without year name
state = make_test_state()
state.year.year_name = ""

result = main_page(state)

assert_equal(
    result.content[1],
    Header("2024", 2)
)

# Test 3: Correct month displayed
state = make_test_state(month=5)
result = main_page(state)

assert_equal(
    result.content[2],
    Header("June", 3)
)


print("All tests completed!")

##############################################

start_server(State(year=forgotten_reams_year, displayed_month=0))
