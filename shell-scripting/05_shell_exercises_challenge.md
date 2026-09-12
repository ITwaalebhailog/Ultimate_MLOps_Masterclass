# Shell Scripting Exercises — Challenge (5 Qs + Answers)

---

## Q1 — Log Monitoring

**Task:**  
Monitor a log file continuously.

**Answer:**

~~~bash
#!/bin/bash

tail -f app.log
~~~

---

## Q2 — Automatic Backup with Date

**Task:**  
Create backup with current date.

**Answer:**

~~~bash
#!/bin/bash

date=$(date +%F)

tar -czf backup_$date.tar.gz myfolder
~~~

---

## Q3 — Disk Alert Script

**Task:**  
Print warning if disk usage > 80%.

**Answer:**

~~~bash
#!/bin/bash

usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $usage -gt 80 ]
then
echo "Disk usage high"
fi
~~~

---

## Q4 — Service Check Script

**Task:**  
Check if docker service is running.

**Answer:**

~~~bash
#!/bin/bash

if systemctl is-active --quiet docker
then
echo "Docker running"
else
echo "Docker stopped"
fi
~~~

---

## Q5 — Automated Folder Creation

**Task:**  
Create project structure automatically.

**Answer:**

~~~bash
#!/bin/bash

mkdir -p mlops_project/{data,models,scripts,logs}
~~~
