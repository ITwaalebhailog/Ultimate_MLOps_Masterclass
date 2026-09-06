# Linux Exercises — Advanced (5 Qs + Answers)

---

## Q1 — Backup script (single command)
**Task:** Create a timestamped tar backup of `mlops_project/` named like `backup_YYYY-MM-DD.tar.gz`.

**Answer:**
~~~bash
ts=$(date +%F) && tar -czf backup_${ts}.tar.gz mlops_project/
ls -lh backup_${ts}.tar.gz
~~~

---

## Q2 — Replace text in many files
**Task:** Replace `PLACEHOLDER` with `PRODUCTION` in all `.conf` files under `config/` (in-place).

**Answer:**
~~~bash
grep -Rl "PLACEHOLDER" config/ | xargs sed -i 's/PLACEHOLDER/PRODUCTION/g'
~~~

---

## Q3 — Monitor log and trigger alert
**Task:** Continuously watch `app.log` and print `ALERT` if `CRITICAL` appears.

**Answer:**
~~~bash
tail -n0 -F app.log | awk '/CRITICAL/ { print strftime("%F %T"), "ALERT:", $0; fflush(); }'
~~~

---

## Q4 — Secure copy large model with resume
**Task:** Copy large `model.tar.gz` to remote `user@server:/models/` with resume support.

**Answer:**
~~~bash
rsync -avP model.tar.gz user@server:/models/
# (rsync does automatic resume; scp is less ideal for resume)
~~~

---

## Q5 — Show network listeners and associated process
**Task:** Show listening ports and the process name/PID (tcp & udp).

**Answer:**
~~~bash
ss -tulpn
# or, if netstat installed:
sudo netstat -tulpn
~~~
