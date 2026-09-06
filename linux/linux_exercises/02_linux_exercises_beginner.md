# Linux Exercises — Beginner (5 Qs + Answers)

Each question has the answer (commands) below it so students can self-check.

---

## Q1 — Create project structure
**Task:** Create this structure:
<img width="262" height="153" alt="image" src="https://github.com/user-attachments/assets/91bda548-739b-417e-add4-b77aaf4c391d" />


**Answer:**
~~~bash
mkdir -p mlops_project/{data,scripts,models}
ls -R mlops_project
~~~

---

## Q2 — Create files
**Task:** Inside `data/` create `data1.csv`, `data2.csv`, `data3.csv`.

**Answer:**
~~~bash
cd mlops_project/data
touch data1.csv data2.csv data3.csv
ls -l
~~~

---

## Q3 — Copy & rename
**Task:** Copy `data1.csv` to repository root as `backup.csv`.

**Answer:**
~~~bash
cp data1.csv ../backup.csv
ls -l ../backup.csv
~~~

---

## Q4 — Show first and last lines
**Task:** Show first 5 and last 5 lines of a (large) log file `app.log`.

**Answer:**
~~~bash
head -n 5 app.log
tail -n 5 app.log
~~~

---

## Q5 — Find hidden files
**Task:** List all files including hidden in your home directory.

**Answer:**
~~~bash
ls -la ~
~~~
