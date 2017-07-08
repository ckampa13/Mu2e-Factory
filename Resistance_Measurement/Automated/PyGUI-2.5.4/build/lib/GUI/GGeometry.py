#
#   Python GUI - Point and rectangle utilities - Generic
#

def add_pt(xxx_todo_changeme, xxx_todo_changeme1):
    (x1, y1) = xxx_todo_changeme
    (x2, y2) = xxx_todo_changeme1
    return (x1 + x2), (y1 + y2)

def sub_pt(xxx_todo_changeme2, xxx_todo_changeme3):
    (x1, y1) = xxx_todo_changeme2
    (x2, y2) = xxx_todo_changeme3
    return (x1 - x2), (y1 - y2)

def rect_sized(xxx_todo_changeme4, xxx_todo_changeme5):
    (l, t) = xxx_todo_changeme4
    (w, h) = xxx_todo_changeme5
    return (l, t, l + w, t + h)

def rect_left(r):
    return r[0]

def rect_top(r):
    return r[1]

def rect_right(r):
    return r[2]

def rect_bottom(r):
    return r[3]

def rect_width(r):
    return r[2] - r[0]

def rect_height(r):
    return r[3] - r[1]

def rect_topleft(r):
    return r[:2]

def rect_botright(r):
    return r[2:]

def rect_center(xxx_todo_changeme6):
    (l, t, r, b) = xxx_todo_changeme6
    return ((l + r) // 2, (t + b) // 2)

def rect_size(xxx_todo_changeme7):
    (l, t, r, b) = xxx_todo_changeme7
    return (r - l, b - t)

def union_rect(xxx_todo_changeme8, xxx_todo_changeme9):
    (l1, t1, r1, b1) = xxx_todo_changeme8
    (l2, t2, r2, b2) = xxx_todo_changeme9
    return (min(l1, l2), min(t1, t2), max(r1, r2), max(b1, b2))

def sect_rect(xxx_todo_changeme10, xxx_todo_changeme11):
    (l1, t1, r1, b1) = xxx_todo_changeme10
    (l2, t2, r2, b2) = xxx_todo_changeme11
    return (max(l1, l2), max(t1, t2), min(r1, r2), min(b1, b2))

def inset_rect(xxx_todo_changeme12, xxx_todo_changeme13):
    (l, t, r, b) = xxx_todo_changeme12
    (dx, dy) = xxx_todo_changeme13
    return (l + dx, t + dy, r - dx, b - dy)

def offset_rect(xxx_todo_changeme14, xxx_todo_changeme15):
    (l, t, r, b) = xxx_todo_changeme14
    (dx, dy) = xxx_todo_changeme15
    return (l + dx, t + dy, r + dx, b + dy)

def offset_rect_neg(xxx_todo_changeme16, xxx_todo_changeme17):
    (l, t, r, b) = xxx_todo_changeme16
    (dx, dy) = xxx_todo_changeme17
    return (l - dx, t - dy, r - dx, b - dy)

def empty_rect(xxx_todo_changeme18):
    (l, t, r, b) = xxx_todo_changeme18
    return r <= l or b <= t

def pt_in_rect(xxx_todo_changeme19, xxx_todo_changeme20):
    (x, y) = xxx_todo_changeme19
    (l, t, r, b) = xxx_todo_changeme20
    return l <= x < r and t <= y < b

def rects_intersect(xxx_todo_changeme21, xxx_todo_changeme22):
    (l1, t1, r1, b1) = xxx_todo_changeme21
    (l2, t2, r2, b2) = xxx_todo_changeme22
    return l1 < r2 and l2 < r1 and t1 < b2 and t2 < b1

def rect_with_center(xxx_todo_changeme23, xxx_todo_changeme24):
    (l, t, r, b) = xxx_todo_changeme23
    (x, y) = xxx_todo_changeme24
    w = r - l
    h = b - t
    rl = x - w // 2
    rt = y - h // 2
    return (rl, rt, rl + w, rt + h)
