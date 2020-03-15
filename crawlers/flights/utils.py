from datetime import datetime

MONTHS = {
    1: 'JANEIRO',
    2: 'FEVEREIRO',
    3: 'MARÇO',
    4: 'ABRIL',
    5: 'MAIO',
    6: 'JUNHO',
    7: 'JULHO',
    8: 'AGOSTO',
    9: 'SETEMBRO',
    10: 'OUTUBRO',
    11: 'NOVEMBRO',
    12: 'DEZEMBRO',
}


def get_date(date):
    dt = datetime.now()
    today = datetime(dt.year, dt.month, dt.day)
    year, month, day = date.split('-')

    try:
        _month = MONTHS.get(int(month), today.month)
        month_int = int(month)
    except ValueError:
        if month.upper() not in MONTHS.values():
            raise
        for key, value in MONTHS.items():
            if value == month.upper():
                month_int = key
                _month = month.upper()
                break
        else:
            raise Exception(f'Invalid month: {month}')

    try:
        _date = datetime(int(year), month_int, int(day))
    except ValueError:
        raise

    if _date < today:
        raise Exception('Date cannot be less than today')
    return _date.year, _month, _date.day
