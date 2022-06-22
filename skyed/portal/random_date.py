from datetime import datetime
import random

def random_date():
    start_date = datetime(2022, 8, 27)
    end_date = datetime(2022, 8, 31)
    rand_date = start_date + (end_date - start_date) * random.random()
    return rand_date    
