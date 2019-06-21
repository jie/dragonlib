import re
from datetime import datetime


def validateDateFormat(dateStr):
    reg = r'^(\d{4})-(\d{2})-(\d{2})$'
    if not re.match(reg, dateStr):
        return False, 'date_format_wrong'

    try:
        datetime.strptime(dateStr, '%Y-%m-%d')
        return True, 'ok'
    except Exception as e:
        return False, 'date_format_error'


def validateTimeFormat(timeStr):
    reg = r'^(\d{2}):(\d{2})$'
    if not re.match(reg, timeStr):
        return False, 'time_format_wrong'
    else:
        return True, 'ok'


def validateDistrict(district):
    reg = r'^(\d+)$'
    if not re.match(reg, str(district)):
        return False, 'district_format_wrong'
    else:
        return True, 'ok'


def validateEmail(email):
    reg = r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$'
    if not re.match(reg, email):
        return False, 'email_format_wrong'
    else:
        return True, 'ok'


def validateDomain(email, domain_config):
    if not domain_config:
        return False, 'avaiable_domain_not_found'

    domain = email.split('@')[1]
    flag = False
    for item in domain_config.data:
        if item == domain:
            flag = True
            break

    if flag:
        return True, 'ok'
    else:
        return False, 'domain_not_avaiable'


def validateMobile(mobile):
    reg = r'^1\d{10}$'
    if not re.match(reg, mobile):
        return False, 'mobilephone_format_wrong'
    else:
        return True, 'ok'


def validatePhone(phone):
    reg = r'^0\d{2,3}-?\d{7,8}$'
    if not re.match(reg, phone):
        return False, 'phone_format_wrong'
    else:
        return True, 'ok'


def validateTimeSequence(start, end):
    start_time = datetime.strptime(
        '2018-01-01 %s' % start, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(
        '2018-01-01 %s' % end, '%Y-%m-%d %H:%M')
    if end_time <= start_time:
        return False, 'time_seq_wrong'
    else:
        return True, 'ok'


def validateDateSequence(start, end):
    if start == end:
        return True, 'ok'
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    if end_date <= start_date:
        return False, 'date_seq_wrong'
    else:
        return True, 'ok'
