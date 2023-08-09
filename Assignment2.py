# Task 1: Data Structures and Algorithms

class Stack():
  def __init__(self,*args) :
    self.stack=[i for i in args]
  def push(self,item):
    self.stack.append(item)
  def pop(self):
    if self.is_empty():
      return "Stack has no elements to remove"
    else:
      el=self.stack.pop()
    return el
  def is_empty(self):
    return len(self.stack)==0
  def size(self):
    return len(self.stack)
  def __str__(self) -> str: # to print stack object in readable format
    return f'Stack: {self.stack}'
  
#Stack impelmented with a pointer at the top of the stack
class StackwithTop():
  def __init__(self,*args) :
    self.stack=[i for i in args]
    self.top=len(args)
  def push(self,item):  
    self.stack.insert(self.top,item)
    self.top+=1
  def pop(self):
    if self.is_empty():
      return  "Stack has no elements to remove"
    else:
      top=self.stack[self.top-1]
      self.top-=1
    return top
  def is_empty(self):
    return self.top==0
  def size(self):
    return self.top+1
  def __str__(self): # to print the object in readable format
    return f'Stack: {self.stack[0:self.top]}'

s=Stack()    
swp=StackwithTop(2,4,5)

print(s)
s.push(2),s.push(3),s.push(4),s.push(5)
print(s)
print("Is stack empty: ",s.is_empty())
s.pop(),s.pop()
print(s)
print("Stack Size: ",s.size())
s.pop(),s.pop(),s.pop()
print("Is stack empty: ",s.is_empty())


print(swp)
swp.pop()
print("Stack size: ",swp.size())
swp.push(6)
print("Is Stack empty: ",swp.is_empty())
swp.pop(),swp.pop(),swp.pop(),swp.pop()
print("Is Stack empty: ",swp.is_empty())

# Task 2: Object-Oriented Programming

class BankAccount():
  def __init__(self,accountNumber, name,balance=0.0):
    self.account_number=accountNumber
    self.account_holder=name
    self.balance=float(balance)
  def deposit(self,amount):
    self.balance+=amount
  def withdraw(self,amount):
    self.balance-=amount
  def get_balance(self):
    return self.balance
  
b1=BankAccount(1234567890,"Sunil",12000)
b2=BankAccount(6354789022,"Joshi")

b1.withdraw(1200)
b2.deposit(1200)

print(f"Balance of {b1.account_number}'s account: ",b1.get_balance())
print(f"Balance of {b2.account_number}'s account: ",b2.get_balance())

b2.withdraw(500)
b1.deposit(700)

print(f"Balance of {b1.account_number}'s account: ",b1.get_balance())
print(f"Balance of {b2.account_number}'s account: ",b2.get_balance())

# Task 3: File Handling and Decorators

import logging
import datetime
# creating a logger with file handler (other than the root) and format as mentioned in the task
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler("logging.txt",'a')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

#s=decorator function to get name and arguments of the function and write it in a log.txt file
def log_file(func):
  def inner(*args,**kwargs):
    global logger
    a=func(*args,**kwargs)
    logging_stmt=f"Funtion name : {func.__name__}, called with arguments :{args,kwargs}"
    logger.info(logging_stmt)  # logs using logging module
    with open("log.txt","a") as f :
      stmt=f"{datetime.datetime.now()} "+logging_stmt+"\n"
      f.write(stmt) #logs written in a simple txt file
    return a
  return inner
  
@log_file
def my_func(*args):  
  return f"Sum of all arguments passed: {sum(args)}"

@log_file
def fibonacci(n,a=0,b=1):
  for _ in range(n-2):
    sum=a+b
    a=b
    b=sum
  return sum

@log_file  
def student_record(n,blg=0,*args,**kwargs):
  name=n
  backlog=blg
  no_of_courses=len(args)
  subjectspassed=list(kwargs.keys())
  total=sum(kwargs.values())
  return (name,backlog,no_of_courses,subjectspassed,total)
 
#function calls to record in the log file
my_func()
my_func(1,2,3,4)
fibonacci(15)
fibonacci(15,2,4)
student_record("Anil")
student_record("Anil",1)
student_record("Anil",1,504,503,506)
student_record("Anil",1,504,503,506,math=67,phy=68)

# Task 4: Advanced Concepts and Libraries

import warnings
warnings.filterwarnings('ignore')
import requests
import random
from matplotlib import pyplot as plt
import re
from PIL import Image

#displaying the returned json in meaningfull manner
def print_info(country):
    cn,on=country['name']['common'],country['name']['official']
    curr=list(country.get('currencies').values())
    capital=country.get('capital')
    pop=country.get('population')/10**6
    con=country.get('continents')
    print(f"\nCountry: {cn} \nOfficial name: {on} \nContinent : {con} \ncapital: {capital} \ncurrency : {curr} \nPopulation: {'%.4f'%pop} M\n")
    
#function to display the iamge as a plot
def display_image(title,path):
  format=r"\.png|gif|jpe?g$"
  if not re.search(format,path):
    print("The Flag link is not an image")
    return
  try:
    img = Image.open(requests.get(path,stream=True).raw) #to access the content of the response in its raw format in chunks
    plt.title(title)
    plt.imshow(img)
    plt.show(block=False)
    plt.pause(3)
    plt.close()
  except Exception as e: # to handle exceptions 
    print("Exception Raised while getting the countries flag")
    print(type(e).__name__, ": ",e)


api = "https://restcountries.com/v3.1/all"
# api = "https://restcountries.com/v3.1/" #raises httperror : url not found
# api = "https:invalid-url.com" # raises invalid url : host not found
# api = "https://url-does-not-exist.com" # raises connection error : name resolution error

ind=random.randint(0,249)
try:
    response= requests.get(api,verify=False)#verify=true raises SSL error : certification not verified
                                            #timeout=0.1 raises timeout error: connect timeout
    response.raise_for_status()
    countries=response.json()
    country=countries[ind]
    print_info(country)
    url=country['flags']['png']
    display_image(f"{country['name']['common']}'s flag",url)
    
#different types of common exceptions caught 
except requests.exceptions.HTTPError as err:
    print("HTTP Error: ", err)
except requests.exceptions.Timeout as err : 
  print("Time out: ", err)
except requests.exceptions.SSLError as err :
  print("SSL error: ", err)
except requests.exceptions.ConnectionError as err :
  print("Connection error: ", err)
except requests.exceptions.InvalidURL as err :
  print("Invalid url: ", err)
except requests.exceptions.ContentDecodingError as err :
  print("Content decoding error: ", err)
except requests.exceptions.JSONDecodeError :
  print("Response recieved is not a valid json")

# Task 5: Algorithmic Problem Solving

#function to return size of LIS using DP with 1D array which stores the length of increasing subsequence including that index element.

def LIS(num):
  if not num:
    return 0
  n = len(num)
  dp = [1] * n
  for i in range(1, n):
    for j in range(i):
      if num[i] > num[j]:
        dp[i] = max(dp[i], dp[j] + 1)
  return max(dp)

print(LIS([3, 1, 5, 2, 4, 9]))

 
  
