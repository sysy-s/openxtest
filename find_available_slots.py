import sys
import os
import platform
from datetime import datetime, timedelta

# gets dates from all users and makes a list that looks like this:
# [
# [
# ['2022-07-02 13:15:00', '2022-06-01 13:59:59'] for alex in the example
# ], 
# ['2022-07-01', ['2022-07-02 00:00:00', '2022-07-02 12:59:59'] for brian in the example
# ]
# ]
# which is a list of excluded time slots
def get_calendars(local_dir):
    dir = os.getcwd() + local_dir
    calendars = []
    for fname in os.listdir(dir):
            fpath = os.path.join(dir, fname)
            if os.path.isfile(fpath):
                with open(fpath, 'r') as file:
                    time_excluded_single_person = []
                    lines = file.readlines()
                    for line in lines:
                        if len(line) <= 12:
                            # converts single date to a time slot ex:
                            # 2022-07-01 -> [2022-07-01 00:00:00, 2022-07-01 23:59:59]
                            # this facilitates date comparison later on
                            date_str = line[:len(line)-1] + ' 00:00:00'
                            date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                            time_excluded_single_person.append([date, date + timedelta(hours=23, minutes=59, seconds=59)])
                        else:
                            # converts string to date
                            slot_start = datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')
                            slot_end = datetime.strptime(line[22:], '%Y-%m-%d %H:%M:%S')
                            time_excluded_single_person.append([slot_start, slot_end])
                    calendars.append(time_excluded_single_person)
    return calendars

def get_available_slots(calendars, duration: int, now: str):
    # we can pick custom start date for testing purposes
    now_slot = [[now, now + timedelta(minutes=duration)]]
    # loop over all the calendars and find time slots after finished meetings:
    # for example: brian finishes at 8:59 so we check if other people are available at 9:00 etc
    available_slots = [now_slot] # list of disponible time slots for possible meetings (those are only the ends of excluded time slots)
    # because the soonest meeting will start right after one ends, so there is no need to search for more
    for personal_calendar in calendars:
        personal_slots = []
        for excluded_time_slot in personal_calendar:
            excluded_slot_end = excluded_time_slot[1]
            available_time_slot = [0,0]
            available_time_slot[0] = excluded_slot_end + timedelta(seconds=1)
            available_time_slot[1] = available_time_slot[0] + timedelta(minutes=duration)
            personal_slots.append(available_time_slot)
        available_slots.append(personal_slots)
    return available_slots

def get_possible_meetings(calendars, available_slots, min_people):
    # next level time complexity
    # finds all meetings that qualify as valid given the command line args
    # it performs a check (whether the meeting collides with a busy slot of another person)
    # for every available slot for every available person
    possible_meetings = [] # list that stores all meetings that satisfy the duration and min people
    for personal_available_slots in available_slots:
        for available_slot in personal_available_slots:
            people_can_attend = 0 # for each slot we count the number of people that can attend the meeting
            for personal_calendar in calendars:
                person_can_attend = True # determines whether 
                for excluded_slot in personal_calendar:
                    # logic that determines whether a time slot overlaps with a potential meeting
                    # meeting overlaps if is starts or ends during the excluded time slot or it starts before and ends after it
                    meeting_ends_during_slot = available_slot[1] >= excluded_slot[0] and available_slot[1] <= excluded_slot[1]
                    meeting_starts_during_slot = available_slot[0] >= excluded_slot[0] and available_slot[0] <= excluded_slot[1]
                    slot_during_meeting = available_slot[0] <= excluded_slot[0] and available_slot[1] >= excluded_slot[1]
                    meeting_overlaps_slot = meeting_ends_during_slot or meeting_starts_during_slot or slot_during_meeting
                    # if meeting overlaps, then the person in question isn't available for this so their state is set to false
                    if meeting_overlaps_slot:
                        person_can_attend = False
                        break # we can break this loop since this person cannot attend this meeting
                if person_can_attend: 
                    people_can_attend += 1 # if none of the busy slots collide with our available meeting we can count this person as valid

            if people_can_attend >= min_people:
                possible_meetings.append(available_slot) # since more people than the minimum can attend we consider this a valid meeting
    return possible_meetings

def get_soonest_meeting(possible_meetings, now):
    # all that's left is to sort the valid meetings and get the first one that isn't in the past
    soonest_meeting = possible_meetings[0][0]
    for meeting in possible_meetings:
        if meeting[0] < soonest_meeting and meeting[0] >= now:
            soonest_meeting = meeting[0]
    return soonest_meeting # message delivery

def main(*argv):
    dir = ''
    duration = 0
    min_people = 0

    # get args and store them in vars
    for i, arg in enumerate(argv):
        match arg:
            case '--calendars':
                dir = argv[i+1]
                if platform.system() == 'Windows':
                    dir = dir.replace('/', '\\')
            case '--duration-in-minutes':
                duration = int(argv[i+1])
            case '--minimum-people':
                min_people = int(argv[i+1])                    
            case _:
                pass
            
    # now = datetime.now().replace(microsecond=0)
    now = datetime(2022, 7, 1, 9, 0, 0)
    calendars = get_calendars(dir)
    available_slots = get_available_slots(calendars, duration, now)
    all_meetings = get_possible_meetings(calendars, available_slots, min_people)
    soonest_meeting = get_soonest_meeting(all_meetings, now)
    print(soonest_meeting)
    
if __name__ == '__main__':
    main(*sys.argv)