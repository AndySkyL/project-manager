from django import template
register = template.Library()
# 此处固定写法，register不能定义为其他的值

# 定义一个过滤器，乘法
@register.filter
def multi(x,y):
    return x * y

# 定义一个标签，乘法
@register.simple_tag
def multi(x,y):
    return x * y