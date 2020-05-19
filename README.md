# Managing LaTeX lecture notes

This repository complements my [third blog post about my note taking setup](https://castel.dev/post/lecture-notes-3).

## A quick overview:

#### File structure

```
ROOT
├── riemann-surfaces
│   ├── info.yaml
│   ├── master.tex
│   ├── lec_01.tex
│   ├── ...
│   ├── lec_13.tex
│   ├── figures
│   │   ├── analytical-continuation-algebraic-equations.pdf
│   │   ├── analytical-continuation-algebraic-equations.pdf_tex
│   │   ├── analytical-continuation-algebraic-equations.svg
│   │   └── ...
│   └── UltiSnips
│       └── tex.snippets
├── selected-topics
└── ...
```

Contents of `info.yaml`
```yaml
title: 'Riemann Surfaces'
short: 'RSurf'
url: 'https://'
```

Contents of  `master.tex`:

```tex
\documentclass[]{report}
\input{../preamble.tex}
\DeclareMathOperator{\Res}{Res}
...
\title{Riemann surfaces}
\begin{document}
    \maketitle
    \tableofcontents
    % start lecture
    \input{lec_01.tex}
    ...
    \input{lec_12.tex}
    % end lectures
\end{document}
```

Here `% start lectures` and `% end lectures` are important.

A lecture file contains a line
```latex
\lecture{1}{vr 14 feb 2020 16:04}{Introduction}
```
which is the lecture number, date an title of the lecture. Date format is configurable in `config.py`.

#### `config.py`

This is where you configure what calendar to use for the countdown script, the root folder of the file structure, and similar stuff. You can also configure the date format used in some places (lecture selection dialog and LaTeX files).
My university uses a system where we label the weeks in a semester from 1 to 13, and this is what the `get_week` function does: it returns the week number of the given date.

#### `courses.py`

This file defines `Course` and `Courses`.
`Courses` is a list of `Course`s in the `ROOT` folder.
A `Course` is a python object that represents a course.
It has a `name`, a `path`, and some `info` (which reads from `info.yaml`).
You can also access its lectures.

`Courses` also has a `current` property which points to the current course.
When setting this property, the script updates the `~/current_course` symlink to point to the current course (configurable in `config.py`)
Furthermore, it writes the short course code to `/tmp/current_course`.
This way, when using polybar, you can add the following to show the current course short code in your panel.

```ini
[module/currentcourse]
type = custom/script
tail = true
exec = echo '/tmp/current_course' | entr cat /tmp/current_course
```


#### `countdown.py`

This script hooks into your calendar, which you can configure in the `config.py` file.
If you're using polybar, you can use the following config:

```ini
[module/calendar]
type = custom/script
exec = TZ='Europe/Brussels' python3 -u ~/scripts/uni/countdown.py
click-left = sensible-browser 'https://calendar.google.com/calendar/' -- &
tail = true
```

It activates the course if the title of the course can be found in the description of the calendar event:
```python
course = next(
    (course for course in courses
     if course.info['title'].lower() in event['summary'].lower()),
    None
)
```

You can easily change this by for example adding a `calendar_name` to each `info.yaml` file and checking with `if course.info['calendar_name'] == event['summary']` or something like that.

To get it working, follow step 1 and 2 of the [Google Calendar Python Quickstart](https://developers.google.com/calendar/quickstart/python), and place `credentials.json` in the `scripts` directory.

#### `lectures.py`

This file defines `Lectures`, the lectures for one course and `Lecture`, a single lecture file `lec_xx.tex`.
A `Lecture` has a `title`, `date`, `week`, which get parsed from the LaTeX source code. It also has a reference to its course.
When calling `.edit()` on a lecture, it opens up lecture in Vim.

`Lectures` is class that inherits from `list` that represents the lectures in one course.
It has a method `new_lecture` which creates a new lecture, `update_lectures_in_master`, which when you call with `[1, 2, 3]` updates `master.tex` to include the first three lectures, `compile_master` which compiles the `master.tex` file.

#### `rofi-courses.py`

When you run this file, it opens rofi allows you to activate a course.

#### `rofi-lectures.py`

When you run this file, it show you lectures of the current course.
Selecting one opens up the file in Vim, pressing `Ctrl+N` creates a new lecture.

#### `rofi-lectures-view.py`

This opens up a rofi dialog to update which lectures are included in `master.tex`

#### `rofi.py`

Wrapper function for rofi

#### `utils.py`

Some utility functions

#### `compile-all-masters.py`

This script updates the `master.tex` files to include all lectures and compiles them. I use when syncing my notes to the cloud. This way I always have access to my compiles notes on my phone.
