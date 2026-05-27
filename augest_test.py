# Deep copy and Shallow Copy

import copy
lst = [1,2,3, [4, 5]]
new_obj = copy.copy(lst)
new_obj[3][0] = 10
print(new_obj)
print(lst)

new_obj1 = copy.deepcopy(lst)
new_obj1[3][0] = 10
print(new_obj1)
print(lst)

# Decorator with time logger
import time
def time_logger(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        print(f"Time taken by function {func.__name__} is {end_time-start_time:.4f}")
        return res
        
    return wrapper
    
@time_logger    
def show_time():
    time.sleep(1)
    return("Done")
    
print(show_time())

#Given an unsorted array of integers, you need to write a program to find the length of the longest consecutive elements sequence.
nums = [100, 4, 200, 1, 3, 2]
# Output: 4

def consecutive_sequence(nums):
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        if num-1 not in num_set:
            current = num
            count = 1
            
            while current + 1 in num_set:
                current+=1
                count+=1
                
            longest = max(longest, count)
            
            
    return longest
    
print(consecutive_sequence(nums))

# Given an array of integers representing the numbers on squares of a chocolate bar, and
# two integers, d (the desired sum) and m (the length of the segment), find the number of
# ways the bar can be divided. A division is valid if a contiguous
# segment of the bar of length m sums to d

s = [2, 2, 1, 3, 2]
d = 4
m = 2

def devide_chocolate_bar(s, d, m):
    count = 0
    for i in range(len(s)-m+1):
        if sum(s[i:i+m]) == d:
            count += 1
            
    return count
    
print(devide_chocolate_bar(s, d, m))

# Given two 2D grids of digits, a large grid G and a smaller pattern grid P, determine if the
# pattern P exists within G.
def grid_search(G, P):
    rows_g = len(G)
    cols_g = len(G[0])
    rows_p = len(P)
    cols_p = len(P[0])
    
    for i in range(rows_g-rows_p+1):
        for j in range(cols_g-cols_p+1):
            found = True
            
            for k in range(rows_p):
                if G[i+k][j:j+cols_p] != P[k]:
                    found = False
                    break
            if found:
                return "Yes"
                
                
    return "No"
    
    
G = [
'7283455864',
'6731158619',
'8988242643',
'3830589324',
'2229505813',
'5633845374',
'6473530293',
'7053106601'
]
P = [
'9505',
'3845',
'3530'
]

print(grid_search(G, P))

# Custom middleware that logsrequest duration
import time
class RequestDurationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start = time.time
        response = self.get_response(request)
        end = time.time()
        print(f"Time taken by the request is {start-end}")
        return response

#Asynchronous route handling in FastAPI?
from fastapi import FastAPI
app = FastAPI()

@app.get('/users')
asynce def get_users():
    return{"response":"User Fetched"}

import numpy as np

arr = np.array([1,2,3])
print(arr+10)


#Transactions work in PostgreSQL and implement a rollback mechanism?    
BEGIN;

UPDATE accounts SET balance = balance-100 WHERE id=1;

ROLLBACK;


#Use Django ORM to run raw SQL queries in PostgreSQL?
from django.db import connection

def get_users:
    with connection.cursor as cursor:
        cursor.execute("SELECT id, username FROM auth_users WHERE id = %s", [True])
        rows = cursor.fetchall()
        
        return rows

# Write a single SQL query that achieves the following task efficiently.
# Task: Calculates the average of the amount within the 7 days window frame

SELECT sale_id, product_id, sale_date, amount,
AVG(amount) OVER (PARTITION BY product_id ORDER BY sale_date
RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW) as avg_amount_last_7_days
FROM Sales
ORDER BY product_id, sale_date;

# Write a SQL query using a Recursive CTE (Recursive Common Table
# Expressions) that fetch hierarchy of provided category "Electronics".

WITH RECURSIVE recursive_tree AS (
    SELECT category_id, category_name, level
    FROM Category
    WHERE category_name = 'Electronics'
    UNION ALL
    SELECT c.category_id, c.category_name, c.level FROM Category c
    INNER JOIN recursive_tree rc ON c.category_id = rc.category_id
    )
SELECT * 
FROM recursive_tree;     









