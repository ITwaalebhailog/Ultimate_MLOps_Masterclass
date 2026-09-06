# Linux Exercises — Intermediate (5 Qs + Answers)

---

## Q1 — Find & count files
**Task:** Find all `.txt` files under current directory and count them.

**Answer:**
~~~bash
find . -type f -name "*.txt" | wc -l
~~~

---

## Q2 — Search text across files
**Task:** Search for the word `ERROR` (case-insensitive) in `logs/` and print file:line.

**Answer:**
~~~bash
grep -Ri --line-number "ERROR" logs/
~~~

---

## Q3 — Disk usage summary
**Task:** Show sizes (human readable) of all top-level folders in the repo sorted by size.

**Answer:**
~~~bash
du -sh ./* | sort -h
~~~

---

## Q4 — Kill by name
**Task:** Find PID(s) of `python` processes belonging to your user and kill them gracefully.

**Answer:**
~~~bash
pgrep -u $(whoami) -f python
# Kill gracefully (by name)
pkill -u $(whoami) -f python
# Or kill specific PID
kill <pid>
~~~

---

## Q5 — Archive old logs
**Task:** Create `logs_archive.tar.gz` containing all `.log` files modified more than 7 days ago.

**Answer:**
~~~bash
find . -type f -name "*.log" -mtime +7 -print0 | tar --null -czf logs_archive.tar.gz --files-from -
ls -lh logs_archive.tar.gz
~~~
