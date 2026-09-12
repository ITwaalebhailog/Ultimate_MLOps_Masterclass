# Shell Scripting Exercises — Advanced (5 Qs + Answers)

---

## Q1 — Loop Through Files

**Task:**  
Print all filenames in a directory.

**Answer:**

~~~bash
#!/bin/bash

for file in *
do
echo $file
done
~~~

---

## Q2 — File Size Check

**Task:**  
Check if file size is greater than 1MB.

**Answer:**

~~~bash
#!/bin/bash

file="data.txt"

size=$(stat -c%s "$file")

if [ $size -gt 1048576 ]
then
echo "File is larger than 1MB"
fi
~~~

---

## Q3 — Process Monitoring

**Task:**  
Check if nginx process is running.

**Answer:**

~~~bash
#!/bin/bash

if pgrep nginx > /dev/null
then
echo "nginx running"
else
echo "nginx not running"
fi
~~~

---

## Q4 — Simple Calculator

**Task:**  
Create a calculator for addition.

**Answer:**

~~~bash
#!/bin/bash

a=10
b=5

echo "Sum = $((a+b))"
~~~

---

## Q5 — Directory Creation Script

**Task:**  
Create directories automatically.

**Answer:**

~~~bash
#!/bin/bash

mkdir project
mkdir project/data
mkdir project/models
mkdir project/scripts
~~~
