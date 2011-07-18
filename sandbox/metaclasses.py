from types import FunctionType

class MetaClass(type):
    def __new__(meta, name, parents, attributes):
        print meta
        ACTIONS = {}
        
        for attribute_name, attribute in attributes.items():
            if type(attribute) == FunctionType and not attribute_name.startswith('__'):
                ACTIONS[attribute_name] = attribute
        
        attributes['ACTIONS'] = ACTIONS
        
        return type.__new__(meta, name, parents, attributes)

class A(object):
    __metaclass__ = MetaClass
    
    def a_method():
        pass
        
class Test(A):
    STEVE_AUSTIN = 5

    def __init__(self):
        pass

    def put_up_or_shut_up(self):
        pass

    classAttribute = 'Something'
    
print A().ACTIONS    
print Test().ACTIONS