from django import template

register = template.Library()


@register.filter
def replace_quotes(value):
    return value.replace("'", '"')

@register.filter
def replace_plus(value):
    return value.replace("+", " ")

@register.filter
def format_date(date):
    # return value.replace("+", " ")
    return date["month"] + ". " + date["day"] + ", " + date["year"] + ", " + date["hour"] + ":" + date["minute"] + " " + date["AM-PM"]

@register.filter
def refer_next(value):
    return value[value.find["next"] + 4: ]