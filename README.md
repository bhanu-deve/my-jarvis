# 🤖 Jarvis Bot — Your Personal GitHub Automation Agent

Run any task automatically on GitHub and get an **email report** (success or failure).

---

## 📁 Project Structure

```
jarvis-bot/
├── jarvis.py                      ← Main agent (your tasks live here)
└── .github/
    └── workflows/
        └── jarvis.yml             ← GitHub Actions (scheduler + trigger)
```

---

## 🚀 Setup in 5 Steps

### Step 1 — Upload to GitHub
1. Create a new GitHub repo (e.g., `my-jarvis`)
2. Upload `jarvis.py` and `.github/workflows/jarvis.yml`

### Step 2 — Create a Gmail App Password
> You CANNOT use your regular Gmail password. You need an **App Password**.

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (required)
3. Search for **"App passwords"**
4. Create a new App Password → choose **Mail** + **Other (Custom name)**
5. Name it `Jarvis Bot` → copy the 16-character password

### Step 3 — Add GitHub Secrets
In your GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name             | Value                          |
|-------------------------|-------------------------------|
| `JARVIS_EMAIL`          | your Gmail address             |
| `JARVIS_EMAIL_PASSWORD` | the 16-char App Password       |
| `JARVIS_NOTIFY_EMAIL`   | email to receive notifications |

### Step 4 — Run It!
**Option A — Manual run:**
- Go to your repo → **Actions** tab
- Click **"Jarvis Bot"** → **"Run workflow"**
- Pick a task → Click **Run**

**Option B — Auto schedule:**
- Already configured! Runs daily at 8:00 AM UTC
- Edit `jarvis.yml` to change the schedule

### Step 5 — Check Your Email 📧
You'll receive a beautiful HTML email with the result!

---

## ✏️ Adding Your Own Tasks

Open `jarvis.py` and add a new function:

```python
def task_my_task() -> str:
    # Your code here
    result = do_something()
    return f"Task done! Result: {result}"
```

Then register it in the `TASKS` dictionary:

```python
TASKS = {
    "hello":         task_hello_world,
    "check_website": task_check_website,
    "scrape_news":   task_scrape_news,
    "custom":        task_custom,
    "my_task":       task_my_task,   # ← add this
}
```

Also add `"my_task"` to the `options` list in `jarvis.yml`.

---

## 📋 Built-in Tasks

| Task           | What it does                              |
|----------------|-------------------------------------------|
| `hello`        | Simple test — confirms Jarvis is working  |
| `check_website`| Pings a URL and reports HTTP status       |
| `scrape_news`  | Fetches top 5 HackerNews stories          |
| `custom`       | Blank task — write your own logic here    |

---

## ⏰ Schedule Examples (cron format)

```yaml
- cron: "0 8 * * *"      # Every day at 8:00 AM UTC
- cron: "0 */6 * * *"    # Every 6 hours
- cron: "0 9 * * 1"      # Every Monday at 9 AM
- cron: "*/30 * * * *"   # Every 30 minutes
- cron: "0 18 * * 1-5"   # Weekdays at 6 PM UTC
```

---

## 💡 Ideas for Custom Tasks

- **Monitor your website** — alert if it goes down
- **Daily weather report** — fetch and email weather for your city
- **Stock price alert** — notify when a stock crosses a threshold
- **Backup data** — export DB and save to GitHub
- **Send WhatsApp/Telegram** — use their APIs inside a task
- **Auto-deploy** — trigger a deployment pipeline
- **Scrape job listings** — find new openings daily
- **Check CouponHive status** — ping your Render backend daily!

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Email not received | Check spam folder; verify App Password is correct |
| Workflow not running | Check Actions tab is enabled in repo settings |
| `Unknown task` error | Make sure task name matches exactly in TASKS dict |
| Gmail auth error | Regenerate App Password; 2FA must be enabled |
