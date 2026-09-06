# Linux Exercises — Challenge (5 Qs + Answers)

These require combining commands and thinking like an SRE.

---

## Q1 — Cleanup large temp files
**Task:** Find and delete files in `/tmp` larger than 100M and log their names to `/var/log/tmp_cleanup.log`.

**Answer:**
~~~bash
sudo find /tmp -type f -size +100M -print -delete | tee -a /var/log/tmp_cleanup.log
~~~

---

## Q2 — Rotate logs manually
**Task:** Rotate `service.log` to `service.log.1` and keep only last 5 rotations.

**Answer:**
~~~bash
# rotate
mv service.log service.log.1
# create new empty log
: > service.log
# keep only 5 rotations (delete older)
ls -1t service.log.* | sed -n '6,$p' | xargs -r rm
~~~

---

## Q3 — Health-check script (exit codes)
**Task:** Write a one-liner that checks if `postgresql` service is active; if not, start it and exit with 0 if started, else exit 2.

**Answer:**
~~~bash
if systemctl is-active --quiet postgresql; then exit 0; else sudo systemctl start postgresql && systemctl is-active --quiet postgresql || exit 2; fi
~~~

---

## Q4 — Atomic upload of model artifact
**Task:** Upload `model.new` to `/srv/models/current` atomically (write to temp then rename).

**Answer:**
~~~bash
# Example using ssh+scp:
scp model.new user@server:/srv/models/model.new.tmp
ssh user@server 'mv /srv/models/model.new.tmp /srv/models/current'
# Local atomic move:
mv model.new /srv/models/model.new.tmp && mv /srv/models/model.new.tmp /srv/models/current
~~~

---

## Q5 — Find config drift (quick diff)
**Task:** Compare `/etc/nginx/nginx.conf` with a baseline at `/opt/baseline/nginx.conf` and print only differing lines.

**Answer:**
~~~bash
diff -u /opt/baseline/nginx.conf /etc/nginx/nginx.conf || true
# For a side-by-side concise view:
sdiff -s /opt/baseline/nginx.conf /etc/nginx/nginx.conf
~~~
