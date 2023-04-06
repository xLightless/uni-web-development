



class Preprocessor(object):
    """ Places scoped data into a preprocessor to use elsewhere """
    
    def __init__(self):
        self.__data = {}
        
    def set_dict(self, data:dict):
        self.__data = data
       
    def get_dict(self):
        return self.__data
    
    
preprocessor = Preprocessor()
        
        
# pre = Preprocessor()


# def func():
#     data = {
#         'test1':'Atest1',
#         'test2':'Atest2'
#     }
    
#     pre.set_dict(data)
    
# func()
    
# print(pre.get_dict())