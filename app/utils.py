def arr_to_numbered_dict(arr):
    dic = {}
    #Use this and not for i in range(), so arr can also be a sqlalchemy search return
    i = 0
    for obj in arr:
        dic[str(i)] = obj
        i+=1
    return dic
