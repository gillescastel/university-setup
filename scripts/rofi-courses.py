#!/usr/bin/python3
from rofi import rofi

from courses import Courses

courses = Courses()
current = courses.current

try:
    current_index = courses.index(current)
    args = ['-a', current_index]
except ValueError:
    args = []

code, index, selected = rofi('Select course', [c.info['title'] for c in courses], [
    '-auto-select',
    '-no-custom',
    '-lines', len(courses)
] + args)

if index >= 0:
    courses.current = courses[index]
