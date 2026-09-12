# Shell Scripting Cheat Sheet

Shell scripting is used to automate tasks in Linux environments.  
It is widely used in **DevOps, MLOps, system administration, and automation pipelines**.

---

# 1. Basic Script Structure

~~~bash
#!/bin/bash

echo "Hello World"
~~~

Run script:

~~~bash
chmod +x script.sh
./script.sh
~~~

---

# 2. Variables

~~~bash
#!/bin/bash

name="mlops"

echo "My name is $name"
~~~

---

# 3. User Input

~~~bash
#!/bin/bash

echo "Enter your name"
read name

echo "Hello $name"
~~~

---

# 4. Command Line Arguments

~~~bash
#!/bin/bash

echo "First argument: $1"
echo "Second argument: $2"
~~~

Run:

~~~bash
./script.sh hello world
~~~

---

# 5. If Condition

~~~bash
#!/bin/bash

num=10

if [ $num -gt 5 ]
then
echo "Number greater than 5"
fi
~~~

---

# 6. If Else Condition

~~~bash
#!/bin/bash

num=3

if [ $num -gt 5 ]
then
echo "Greater"
else
echo "Smaller"
fi
~~~

---

# 7. For Loop

~~~bash
#!/bin/bash

for i in 1 2 3 4 5
do
echo $i
done
~~~

---

# 8. While Loop

~~~bash
#!/bin/bash

i=1

while [ $i -le 5 ]
do
echo $i
((i++))
done
~~~

---

# 9. Functions

~~~bash
#!/bin/bash

hello() {
echo "Hello world"
}

hello
~~~

---

# 10. Exit Codes

~~~bash
#!/bin/bash

if [ $? -eq 0 ]
then
echo "Command successful"
else
echo "Command failed"
fi
~~~

---

# 11. File Checking

~~~bash
#!/bin/bash

if [ -f file.txt ]
then
echo "File exists"
else
echo "File not found"
fi
~~~

---

# 12. Useful Operators

| Operator | Meaning |
|--------|--------|
| -eq | equal |
| -ne | not equal |
| -gt | greater than |
| -lt | less than |
| -ge | greater or equal |
| -le | less or equal |

---
