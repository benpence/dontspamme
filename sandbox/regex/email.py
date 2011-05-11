import re

pattern = re.compile(
    # Name
    r'\"?'
    r'(?P<name>.(:?\w+\s*)+)?'
    r'\"?'

    r'\s*'

    # Email address
    r'\<?(?P<email>(?P<mask>\w+)(:?\+(?P<contact>\w+))?@(?P<domain>(:?\w+\.)+\w+))'
    r'\>?$'
)

m = pattern.search('"Ben Pence" <ben+ee@dicksdicksdicks.com>')
print m.group('name')
print m.group('mask')
print m.group('contact')
print m.group('domain')
