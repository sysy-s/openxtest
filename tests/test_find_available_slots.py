import platform
import datetime
from ..find_available_slots import get_calendars, get_available_slots, get_possible_meetings, get_soonest_meeting


def test_get_calendars_vanilla():
    calendars = [[
                [datetime.datetime(2022, 7, 2, 13, 15), datetime.datetime(2022, 7, 2, 13, 59, 59)]],
        [[datetime.datetime(2022, 7, 1, 0, 0), datetime.datetime(2022, 7, 1, 23, 59, 59)],
         [datetime.datetime(2022, 7, 2, 0, 0), datetime.datetime(2022, 7, 2, 12, 59, 59)]]]
    if platform.system() == 'Windows':
        assert get_calendars('\\tests\\calendars1') == calendars
    else:
        assert get_calendars('/tests/calendars1') == calendars


def test_get_calendars_empty_dir():
    calendars = []

    if platform.system() == 'Windows':
        assert get_calendars('\\tests\\calendars2') == calendars
    else:
        assert get_calendars('/tests/calendars2') == calendars


def test_get_calendars_single_dates_only():
    calendars = [[
        [datetime.datetime(2022, 7, 1, 0, 0),
         datetime.datetime(2022, 7, 1, 23, 59, 59)],
        [datetime.datetime(2022, 7, 3, 0, 0),
         datetime.datetime(2022, 7, 3, 23, 59, 59)],
        [datetime.datetime(2022, 7, 4, 0, 0),
         datetime.datetime(2022, 7, 4, 23, 59, 59)],
        [datetime.datetime(2022, 8, 17, 0, 0),
         datetime.datetime(2022, 8, 17, 23, 59, 59)],
        [datetime.datetime(2023, 2, 1, 0, 0),
         datetime.datetime(2023, 2, 1, 23, 59, 59)],
        [datetime.datetime(2023, 2, 28, 0, 0),
         datetime.datetime(2023, 2, 28, 23, 59, 59)],
        [datetime.datetime(2023, 8, 2, 0, 0), datetime.datetime(2023, 8, 2, 23, 59, 59)]],
        [[datetime.datetime(2022, 7, 5, 0, 0), datetime.datetime(2022, 7, 5, 23, 59, 59)],
         [datetime.datetime(2022, 5, 23, 0, 0),
          datetime.datetime(2022, 5, 23, 23, 59, 59)],
         [datetime.datetime(2022, 4, 16, 0, 0),
          datetime.datetime(2022, 4, 16, 23, 59, 59)],
         [datetime.datetime(2022, 6, 1, 0, 0), datetime.datetime(2022, 6, 1, 23, 59, 59)]],
        [[datetime.datetime(2022, 7, 1, 0, 0), datetime.datetime(2022, 7, 1, 23, 59, 59)],
         [datetime.datetime(2022, 7, 3, 0, 0),
          datetime.datetime(2022, 7, 3, 23, 59, 59)],
         [datetime.datetime(2022, 7, 4, 0, 0),
          datetime.datetime(2022, 7, 4, 23, 59, 59)],
         [datetime.datetime(2022, 8, 1, 0, 0), datetime.datetime(2022, 8, 1, 23, 59, 59)]]]

    if platform.system() == 'Windows':
        assert get_calendars('\\tests\\calendars3') == calendars
    else:
        assert get_calendars('/tests/calendars3') == calendars

def test_available_slots_vanilla():
    calendars = []
    if platform.system() == 'Windows':
        calendars = get_calendars('\\tests\\calendars1')
    else:
        calendars = get_calendars('/tests/calendars1')
    duration = 30
    now = datetime.datetime(2022, 7, 1, 9, 0, 0)
    available_slots = [[[now, now + datetime.timedelta(minutes=duration)]],
                       [[datetime.datetime(2022, 7, 2, 14, 0), datetime.datetime(2022, 7, 2, 14, 30)]],
                       [[datetime.datetime(2022, 7, 2, 0, 0), datetime.datetime(2022, 7, 2, 0, 30)],
                        [datetime.datetime(2022, 7, 2, 13, 0), datetime.datetime(2022, 7, 2, 13, 30)]]]
    assert get_available_slots(calendars, duration, now) == available_slots

def test_available_slots_empty_dir():
    calendars = []
    duration = 30
    now = datetime.datetime(2022, 7, 1, 9, 0, 0)
    available_slots = [[[now, now + datetime.timedelta(minutes=duration)]]]
    assert get_available_slots(calendars, duration, now) == available_slots

def test_available_slots_single_dates_only():
    calendars = []
    if platform.system() == 'Windows':
        calendars = get_calendars('\\tests\\calendars3')
    else:
        calendars = get_calendars('/tests/calendars3')
    duration = 30
    now = datetime.datetime(2022, 7, 1, 9, 0, 0)
    available_slots = [[[now, now + datetime.timedelta(minutes=duration)]], 
                        [[datetime.datetime(2022, 7, 2, 0, 0), datetime.datetime(2022, 7, 2, 0, 30)], 
                        [datetime.datetime(2022, 7, 4, 0, 0), datetime.datetime(2022, 7, 4, 0, 30)], 
                        [datetime.datetime(2022, 7, 5, 0, 0), datetime.datetime(2022, 7, 5, 0, 30)], 
                        [datetime.datetime(2022, 8, 18, 0, 0), datetime.datetime(2022, 8, 18, 0, 30)], 
                        [datetime.datetime(2023, 2, 2, 0, 0), datetime.datetime(2023, 2, 2, 0, 30)], 
                        [datetime.datetime(2023, 3, 1, 0, 0), datetime.datetime(2023, 3, 1, 0, 30)], 
                        [datetime.datetime(2023, 8, 3, 0, 0), datetime.datetime(2023, 8, 3, 0, 30)]],
                        [[datetime.datetime(2022, 7, 6, 0, 0), datetime.datetime(2022, 7, 6, 0, 30)], 
                        [datetime.datetime(2022, 5, 24, 0, 0), datetime.datetime(2022, 5, 24, 0, 30)], 
                        [datetime.datetime(2022, 4, 17, 0, 0), datetime.datetime(2022, 4, 17, 0, 30)], 
                        [datetime.datetime(2022, 6, 2, 0, 0), datetime.datetime(2022, 6, 2, 0, 30)]], 
                        [[datetime.datetime(2022, 7, 2, 0, 0), datetime.datetime(2022, 7, 2, 0, 30)], 
                        [datetime.datetime(2022, 7, 4, 0, 0), datetime.datetime(2022, 7, 4, 0, 30)], 
                        [datetime.datetime(2022, 7, 5, 0, 0), datetime.datetime(2022, 7, 5, 0, 30)], 
                        [datetime.datetime(2022, 8, 2, 0, 0), datetime.datetime(2022, 8, 2, 0, 30)]]]
    assert get_available_slots(calendars, duration, now) == available_slots

def test_get_possible_meetings_vanilla():
    calendars = []
    if platform.system() == 'Windows':
        calendars = get_calendars('\\tests\\calendars1')
    else:
        calendars = get_calendars('/tests/calendars1')
    duration = 30
    min_people = 2
    now = datetime.datetime(2022, 7, 1, 9, 0, 0)
    available_slots = get_available_slots(calendars, duration, now)
    possible_meetings = [[datetime.datetime(2022, 7, 2, 14, 0), datetime.datetime(2022, 7, 2, 14, 30)]]
    assert get_possible_meetings(calendars, available_slots, min_people) == possible_meetings

def test_get_possible_meetings_empty_dir():
    calendars = []
    duration = 30
    min_people = 2
    now = datetime.datetime.now().replace(microsecond=0)
    available_slots = get_available_slots(calendars, duration, now)
    assert get_possible_meetings(calendars, available_slots, min_people) == []

def test_get_soonest_meeting_vanilla():
    calendars = []
    if platform.system() == 'Windows':
        calendars = get_calendars('\\tests\\calendars1')
    else:
        calendars = get_calendars('/tests/calendars1')
    duration = 30
    min_people = 2
    now = datetime.datetime(2022, 7, 1, 9, 0, 0)
    available_slots = get_available_slots(calendars, duration, now)
    possible_meetings = get_possible_meetings(calendars, available_slots, min_people)
    assert get_soonest_meeting(possible_meetings, now) == datetime.datetime(2022, 7, 2, 14, 0, 0)

def test_get_soonest_meeting_empty_dir():
    calendars = []
    duration = 30
    min_people = 2
    now = datetime.datetime(2022, 7, 1, 9, 0, 0)
    available_slots = get_available_slots(calendars, duration, now)
    possible_meetings = get_possible_meetings(calendars, available_slots, min_people)
    assert get_soonest_meeting(possible_meetings, now) == now

def test_get_soonest_meeting_before_today():
    calendars = []
    if platform.system() == 'Windows':
        calendars = get_calendars('\\tests\\calendars1')
    else:
        calendars = get_calendars('/tests/calendars1')
    duration = 30
    min_people = 2
    now = datetime.datetime(2022, 7, 3, 9, 0, 0)
    available_slots = get_available_slots(calendars, duration, now)
    possible_meetings = get_possible_meetings(calendars, available_slots, min_people)
    assert get_soonest_meeting(possible_meetings, now) == datetime.datetime(2022, 7, 3, 9, 0, 0)