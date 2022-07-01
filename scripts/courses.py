#!/usr/bin/python3
from pathlib import Path
import yaml

from lectures import Lectures
from config import ROOT, CURRENT_COURSE_ROOT, CURRENT_COURSE_SYMLINK, CURRENT_COURSE_WATCH_FILE

class Course():
    def __init__(self, path):
        self.path = path
        self.name = path.stem

        self.info = yaml.safe_load((path / 'info.yaml').open())
        self._lectures = None

    @property
    def lectures(self):
        if not self._lectures:
            self._lectures = Lectures(self)
        return self._lectures

    def __eq__(self, other):
        if other == None:
            return False
        return self.path == other.path

class Courses(list):
    def __init__(self):
        list.__init__(self, self.read_files())

    def read_files(self):
        course_directories = [x for x in ROOT.iterdir() if x.is_dir()]
        _courses = [Course(path) for path in course_directories]
        return sorted(_courses, key=lambda c: c.name)

    @property
    def current(self):
        return Course(CURRENT_COURSE_ROOT.resolve())

    @current.setter
    def current(self, course):
        CURRENT_COURSE_SYMLINK.unlink()
        CURRENT_COURSE_SYMLINK.symlink_to(course.path)
        CURRENT_COURSE_WATCH_FILE.write_text('{}\n'.format(course.info['short']))
