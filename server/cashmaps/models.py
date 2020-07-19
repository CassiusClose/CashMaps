from cashmaps import app

def results_to_arr(results):
    """Returns the results of a query() call as an array, with each object in a dictionary format"""
    arr = []
    for r in results:
        arr.append(r.to_dict())
    return arr
