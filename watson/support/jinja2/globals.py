# -*- coding: utf-8 -*-


def get_current_date():
    import datetime
    return datetime.date.today().strftime("%d.%m.%Y")
