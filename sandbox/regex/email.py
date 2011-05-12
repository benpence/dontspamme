import re

name_pattern = re.compile(
    r'\"?'
    r'(?P<name>.(:?\w+\s*)+)?'
    r'\"?'
    r'\s*'
)

email_pattern = re.compile(
    r'\<?'
    r'(?P<email>(?P<user>\w+)(:?\+(?P<contact>\w+))?@(?P<domain>(:?\w+\.)+\w+))'
    r'\>?$'
)

original = '"Ben Pence" test+ee@di.com'

separator = original.rfind(' ') + 1

m = name_pattern.search(original[:separator])
print m.group('name')

m = email_pattern.search(original[separator:])
print m.group('email')
print m.group('user')
print m.group('contact')
print m.group('domain')
