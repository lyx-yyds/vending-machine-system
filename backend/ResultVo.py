class ResultVo:
    def success(message,data=None):
        return {
            'code':2000,
            'message':message,
            'data':data
            
        }
    
    def faild(message,code=2001):
        return {
            'code':code,
            'message':message,
            'data':None
        }  