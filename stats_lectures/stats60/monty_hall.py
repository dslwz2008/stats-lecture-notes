from base64 import encodestring
from pkg_resources import resource_stream

import numpy as np
from IPython.core.display import HTML

from examples import example

height, width = 120, 120
host_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
             (height, 
              width,
              encodestring(resource_stream('stats_lectures', \
                           'data/host.png').read()).decode('ascii')))

student_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
                (height,
                 width,
                 encodestring(resource_stream('stats_lectures', \
                              'data/user-student.png').read()).decode('ascii')))

student_win_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
                    (height,
                     width,
                     encodestring(resource_stream('stats_lectures', \
                                  'data/student_win.png').read()).decode('ascii')))

student_lose_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
                     (height,
                      width,
                      encodestring(resource_stream('stats_lectures', \
                                  'data/student_lose.png').read()).decode('ascii')))

car_html = ('<img height="%d" width="%d" src="data:image/png;base64,%s">' % 
            (height,
             width,
             encodestring(resource_stream('stats_lectures', \
                          'data/310px-Car_with_Driver-Silhouette.svg.png' \
                                         ).read()).decode('ascii')))

def monty_hall_table(car_pos, student_pos, host_pos, final_pos=None):

    def make_row(label, img, pos):
        row = (('<tr><td width="%d"><h2 align="center">%s</h2></td>' % (width, label)) + 
               ('<td height="%d" width="%d"></td>' % (height, width)) * pos
               + ('<td height="%d" width="%d">%s</td>' % (height, width, img))
               + ('<td height="%d" width="%d"></td>' % (height, width)) * (2-pos) + '</tr>')
        return row

    if final_pos is not None:
        if car_pos == final_pos:
            final_row = make_row('Final', student_win_html, final_pos)
        else:
            final_row = make_row('Final', student_lose_html, final_pos)
    else:
        final_row = ''
    table = '\n'.join(['<table>',
                       make_row('Prize', car_html, car_pos),
                       make_row('Student', student_html, student_pos),
                       make_row('Host', host_html, host_pos),
                       final_row,
                       '</table>'])
    return table

class monty_hall_example(example):

    """
    The no-switching strategy as default
    """

    def __init__(self, rule = lambda student, host: student):
        self.draw_sample()
        self.rule = rule
        self.reset()

    def draw_sample(self):
        self.car, self.student = np.random.random_integers(0,2,size=(2,))
        if self.car == self.student:
            host_sample_space = list(set(range(3)).difference([self.car]))
            self.host = host_sample_space[np.random.random_integers(0,1)]
        else:
            self.host = list(set(range(3)).difference([self.car, self.student]))[0]

    def trial(self, numeric=False):
        self.draw_sample()

        self.final = self.rule(self.student, self.host)

        self.outcome = (self.car, self.student)
        self.numeric_outcome = self.final == self.car

        self.total += self.numeric_outcome
        self.ntrial += 1

        if numeric:
            return self.numeric_outcome
        return self.outcome

    def _repr_html_(self):
        if self.outcome is None:
            base = monty_hall_table(self.car, 
                                    self.student,
                                    self.host,
                                    None)
        else:
            base = monty_hall_table(self.car, 
                                    self.student,
                                    self.host,
                                    self.final)

        if self.ntrial > 0:
            base += '<h3>Success rate: %d out of %d: %d%%</h3>' % (self.total, self.ntrial, 100*self.mean)
        return base

class conditional_nomatch(monty_hall_example):
    
    """
    We draw samples until initial student guess does not match the car.
    """

    def draw_sample(self):
        while True:
            monty_hall_example.draw_sample(self)
            if self.student != self.car:
                break

class conditional_match(monty_hall_example):
    
    """
    We draw samples until initial student matches the car.
    """

    def draw_sample(self):
        while True:
            monty_hall_example.draw_sample(self)
            if self.student != self.car:
                break


no_switch = monty_hall_example()

def switch_rule(student, host):
    return list(set(range(3)).difference([student, host]))[0]
switch = monty_hall_example(rule=switch_rule)

def conditional_stratgy(do_switch, do_match):
    if do_match:
        if do_switch:
            return conditional_match(rule=switch_rule)
        return conditional_match()
    else:
        if do_switch:
            return conditional_nomatch(rule=switch_rule)
        return conditional_nomatch()
        