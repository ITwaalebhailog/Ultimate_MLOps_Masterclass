# Shell Scripting Exercises — Intermediate (5 Qs + Answers)

---

## Q1 — File Exists Check

**Task:**  
Write a script to check if a file exists.

**Answer:**

~~~bash
#!/bin/bash

file="data.txt"

if [ -f $file ]
then
echo "File exists"
else
echo "File not found"
fi
~~~

---

## Q2 — Count Files

**Task:**  
Write a script that counts files in the current directory.

**Answer:**

~~~bash
#!/bin/bash

count=$(ls | wc -l)

echo "Total files: $count"
~~~

---

## Q3 — Print Even Numbers

**Task:**  
Write a script that prints even numbers from 1 to 10.

**Answer:**

~~~bash
#!/bin/bash

for i in {1..10}
do
if [ $((i%2)) -eq 0 ]
then
echo $i
fi
done
~~~

---

## Q4 — Backup Script

**Task:**  
Create a backup of a folder.

**Answer:**

~~~bash
#!/bin/bash

tar -czf backup.tar.gz myfolder
~~~

---

## Q5 — Check Disk Usage

**Task:**  
Write a script that prints disk usage.

**Answer:**

~~~bash
#!/bin/bash

df -h
~~~
