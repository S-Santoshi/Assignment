#Task 1: Lists and Tuples

fruits = ["apple", "banana", "orange", "grape"]
fruits.append("watermelon")
print(len(fruits))
colors=("Red","Green","Blue")
print(colors[1])

# Task 2: Dictionaries and Sets

student={"name": "S Santoshi","age": 20,"university":"VIIT"}
print(student["age"])
skills={"Programming and Coding","problem solving","Continuous learning"}
skills.add("Machine learning")
print(len(skills))

# Task 3: Data Structures and Functions

class Book():
  def __init__(self,title,author,year) : #constructor to initialize the objects attribute
    self.title=title
    self.author=author
    self.year=year
  def print_book_info(self):
    print(f"The Book's Title is {self.title} written by {self.author}, published in the year{self.year}")
    
book1=Book("Invisible","James Patterson",2013)
book1.print_book_info()

# Task 4: Itertools

import itertools
numbers=[1,2,3]
for i in itertools.permutations(numbers): #the function returns a iterator that is parsed to print the permutation 
  print(i)
  
# Task 5: Decorators

import time
#decorator function to calculate the time taken
def measure_time(func1):
  def inner(n):
    start=time.time()
    func1(n)
    end=time.time()
    time_elapsed=end-start
    print(f"Time taken to execute the decorated function {func1.__name__} is ", time_elapsed,"s")
  return inner

#function to calculate the nth term of fibonaaci series 
@measure_time
def fibonacci(n):
  a,b=0,1
  for _ in range(n-2):
    sum=a+b
    a=b
    b=sum
  #print(sum)

#function to calculate the  n factorial 
@measure_time    
def factorial(n):
  ans=1
  while n>1:
    ans*=n
    n-=1
  #print(ans)
    
fibonacci(10000)
factorial(10000)