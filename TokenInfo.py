class token:
    value=''
    is_open=0
    is_close=0
    index=-1
    is_name=0

    def __init__(self,value,is_open,is_close,is_name,index):
        self.value=value
        self.is_close=is_close
        self.is_open=is_open
        self.is_name=is_name
        self.index=index

