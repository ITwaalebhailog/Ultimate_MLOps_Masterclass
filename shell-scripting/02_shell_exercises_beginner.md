# Shell Scripting Exercises — Beginner (5 Qs + Answers)

---

## Q1 — Hello World Script

**Task:**  
Write a shell script that prints:

Hello Welcome to MLOps Masterclass

**Answer:**

~~~bash
#!/bin/bash

echo "Hello Welcome to MLOps Masterclass"
~~~

---

## Q2 — Variable Script

**Task:**  
Create a script that stores your name in a variable and prints it.

**Answer:**

~~~bash
#!/bin/bash

name="MLOps"

echo "My name is $name"
~~~

---

## Q3 — User Input Script

**Task:**  
Ask the user for their name and greet them.

**Answer:**

~~~bash
#!/bin/bash

echo "Enter your name"
read name

echo "Hello $name"
~~~

---

## Q4 — Print Numbers

**Task:**  
Write a script to print numbers from 1 to 5.

**Answer:**

~~~bash
#!/bin/bash

for i in 1 2 3 4 5
do
echo $i
done
~~~

---

## Q5 — Simple Condition

**Task:**  
Write a script that checks if a number is greater than 10.

**Answer:**

~~~bash
#!/bin/bash

num=12

if [ $num -gt 10 ]
then
echo "Number is greater than 10"
fi
~~~
