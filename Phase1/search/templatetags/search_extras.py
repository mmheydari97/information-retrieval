from django import template

register = template.Library()


@register.filter(name='farsi_date')
def farsi_date(value):
    parts = str(value).split()
    day = parts[0]
    month = parts[2]

    if day.lower() == "sat":
        parts[0] = "شنبه"
    elif day.lower() == "sun":
        parts[0] = "یکشنبه"
    elif day.lower() == "mon":
        parts[0] = "دوشنبه"
    elif day.lower() == "tue":
        parts[0] = "سه‌شنبه"
    elif day.lower() == "wed":
        parts[0] = "چهارشنبه"
    elif day.lower() == "thu":
        parts[0] = "پنج‌شنبه"
    elif day.lower() == "fri":
        parts[0] = "جمعه"

    if month.lower() == "jan":
        parts[2] = "ژانویه"
    elif month.lower() == "feb":
        parts[2] = "فوریه"
    elif month.lower() == "mar":
        parts[2] = "مارس"
    elif month.lower() == "apr":
        parts[2] = "آوریل"
    elif month.lower() == "may":
        parts[2] = "مه"
    elif month.lower() == "jun":
        parts[2] = "ژوئن"
    elif month.lower() == "jul":
        parts[2] = "ژوئیه"
    elif month.lower() == "aug":
        parts[2] = "اوت"
    elif month.lower() == "sep":
        parts[2] = "سپتامبر"
    elif month.lower() == "oct":
        parts[2] = "اکتبر"
    elif month.lower() == "nov":
        parts[2] = "نوامبر"
    elif month.lower() == "dec":
        parts[2] = "دسامبر"

    return "{}، {} {} {}".format(parts[0], parts[1], parts[2], parts[3])
