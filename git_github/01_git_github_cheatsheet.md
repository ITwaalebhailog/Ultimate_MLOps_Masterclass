# Git + GitHub Cheat Sheet

Git is used for **version control**, while GitHub is used for **remote collaboration**.

---

# 1. Git Setup

Check git version

~~~bash
git --version
~~~

Configure username

~~~bash
git config --global user.name "Your Name"
~~~

Configure email

~~~bash
git config --global user.email "you@email.com"
~~~

---

# 2. Repository Initialization

Initialize repo

~~~bash
git init
~~~

Clone repository

~~~bash
git clone repo_url
~~~

---

# 3. Basic Workflow

Check status

~~~bash
git status
~~~

Add file

~~~bash
git add file.txt
~~~

Add all files

~~~bash
git add .
~~~

Commit changes

~~~bash
git commit -m "initial commit"
~~~

Push to GitHub

~~~bash
git push origin main
~~~

Pull latest changes

~~~bash
git pull origin main
~~~

---

# 4. Branching

Create branch

~~~bash
git branch feature1
~~~

Switch branch

~~~bash
git checkout feature1
~~~

Create and switch

~~~bash
git checkout -b feature1
~~~

Merge branch

~~~bash
git merge feature1
~~~

Delete branch

~~~bash
git branch -d feature1
~~~

---

# 5. Remote Repositories

Add remote

~~~bash
git remote add origin repo_url
~~~

Check remotes

~~~bash
git remote -v
~~~

---

# 6. Git Logs

View history

~~~bash
git log
~~~

Compact log

~~~bash
git log --oneline
~~~

---

# 7. Undo Changes

Unstage file

~~~bash
git reset file.txt
~~~

Discard changes

~~~bash
git checkout -- file.txt
~~~
