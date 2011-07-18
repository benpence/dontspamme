class FormatError(Exception):
    def __init__(self, key):
        self.value = "Invalid %s" % key
    def __str__(self):
        return repr(self.value)

def decorator_with_state(decorator):
    def uninitialized_decorator(*dec_args, **dec_kwargs):
        def initialized_decorator(decorated_method):
            def instance_method(self, *instance_args, **instance_kwargs):
                decorator(*((self, decorated_method) + instance_args + dec_args), **dict(instance_kwargs.items() + dec_kwargs.items()))
            return instance_method
        return initialized_decorator
    return uninitialized_decorator

@decorator_with_state
def admin_access(person, method):
    is_admin = lambda: True
    
    print 'Checking credentials'
    
    method(person, is_admin=is_admin())

@decorator_with_state
def require(person, method, is_admin=False, **require_types):
    if is_admin:
        print 'You have administrative access'
    
    for key in require_types:
        if key not in person.values:
            raise FormatError(key)
            
        try:
            setattr(
                person,
                key,
                require_types[key](
                    person.values[key]
                )
            )
        except ValueError:
            raise FormatError(key)
    
    method(person)
                
class Person(object):
    def __init__(self, **values):
        self.values = values
        
    @admin_access()
    @require(age=int)
    def submit(self, age=None):
        print person.age

if __name__ == '__main__':
    person = Person(age='a')
    
    try:
        person.submit()
        
    except FormatError as e:
        print e.value