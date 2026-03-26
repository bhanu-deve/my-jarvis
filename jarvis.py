"""
JARVIS - Your Personal AI Automation Agent
Runs on GitHub Actions and emails you the results.
"""

import os
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


# ─────────────────────────────────────────
#  EMAIL NOTIFICATION
# ─────────────────────────────────────────

def send_email(subject: str, body_html: str, success: bool):
    """Send result email via Gmail SMTP."""
    sender     = os.environ["JARVIS_EMAIL"]          # your Gmail
    password   = os.environ["JARVIS_EMAIL_PASSWORD"]  # Gmail App Password
    recipient  = os.environ.get("JARVIS_NOTIFY_EMAIL", sender)  # who to notify

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Jarvis Bot <{sender}>"
    msg["To"]      = recipient

    status_color = "#22c55e" if success else "#ef4444"
    status_text  = "✅ SUCCESS" if success else "❌ FAILED"

    html = f"""
    <html><body style="font-family:Arial,sans-serif;background:#0f172a;color:#e2e8f0;padding:20px;">
      <div style="max-width:600px;margin:auto;background:#1e293b;border-radius:12px;
                  border:1px solid #334155;overflow:hidden;">
        <div style="background:{status_color};padding:20px;text-align:center;">
          <h1 style="margin:0;color:#fff;font-size:24px;">🤖 JARVIS REPORT</h1>
          <p style="margin:8px 0 0;color:#fff;font-size:18px;font-weight:bold;">{status_text}</p>
        </div>
        <div style="padding:24px;">
          <p style="color:#94a3b8;margin-top:0;">
            <strong>Time:</strong> {datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")}
          </p>
          <hr style="border-color:#334155;margin:16px 0;">
          <div style="background:#0f172a;border-radius:8px;padding:16px;
                      font-family:monospace;font-size:14px;white-space:pre-wrap;">
{body_html}
          </div>
        </div>
        <div style="padding:16px 24px;border-top:1px solid #334155;text-align:center;
                    color:#475569;font-size:12px;">
          Jarvis Bot · GitHub Actions · Auto-generated report
        </div>
      </div>
    </body></html>
    """

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print(f"📧 Email sent to {recipient}")
    except Exception as e:
        print(f"⚠️  Email failed: {e}")


# ─────────────────────────────────────────
#  YOUR TASKS — Add / Edit these freely!
# ─────────────────────────────────────────

def task_hello_world() -> str:
    """Simple demo task."""
    print("Running: Hello World Task")
    return "Hello from Jarvis! 👋\nThis is your first automated task."


def task_check_website() -> str:
    """Check if a website is reachable."""
    import urllib.request
    url = os.environ.get("JARVIS_CHECK_URL", "https://google.com")
    print(f"Running: Website Check → {url}")
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            code = r.getcode()
        return f"Website check PASSED ✅\nURL   : {url}\nStatus: {code} OK"
    except Exception as e:
        raise RuntimeError(f"Website check FAILED ❌\nURL: {url}\nError: {e}")


def task_scrape_news() -> str:
    """Fetch top headlines from HackerNews API."""
    import urllib.request, json
    print("Running: Fetch HackerNews Top Stories")
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    with urllib.request.urlopen(url, timeout=10) as r:
        ids = json.loads(r.read())[:5]

    lines = ["🗞  Top 5 HackerNews Stories\n"]
    for i, story_id in enumerate(ids, 1):
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        with urllib.request.urlopen(item_url, timeout=10) as r:
            item = json.loads(r.read())
        title = item.get("title", "N/A")
        link  = item.get("url", f"https://news.ycombinator.com/item?id={story_id}")
        lines.append(f"{i}. {title}\n   {link}")

    return "\n".join(lines)


def task_custom() -> str:
    """
    🔧 YOUR CUSTOM TASK — Edit this to do anything you want!
    Examples:
      - Call an API and save results
      - Process files in the repo
      - Run database queries
      - Send WhatsApp / Telegram messages
      - Deploy something
    """
    print("Running: Custom Task")

    # ✏️  WRITE YOUR CODE HERE
    result = "Custom task ran successfully!\nReplace this with your own logic."
    return result


# ─────────────────────────────────────────
#  TASK REGISTRY — Map names → functions
# ─────────────────────────────────────────

TASKS = {
    "hello":         task_hello_world,
    "check_website": task_check_website,
    "scrape_news":   task_scrape_news,
    "custom":        task_custom,
}


# ─────────────────────────────────────────
#  MAIN RUNNER
# ─────────────────────────────────────────

def main():
    task_name = os.environ.get("JARVIS_TASK", "hello")
    print(f"\n{'='*50}")
    print(f"  🤖 JARVIS STARTING — Task: {task_name}")
    print(f"  Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"{'='*50}\n")

    if task_name not in TASKS:
        available = ", ".join(TASKS.keys())
        msg = f"Unknown task: '{task_name}'\nAvailable tasks: {available}"
        print(f"❌ {msg}")
        send_email(f"[Jarvis] ❌ Unknown Task: {task_name}", msg, success=False)
        exit(1)

    try:
        output = TASKS[task_name]()
        print(f"\n✅ Task completed successfully:\n{output}")
        send_email(
            subject=f"[Jarvis] ✅ Task '{task_name}' Completed",
            body_html=output,
            success=True
        )
    except Exception as e:
        error_detail = traceback.format_exc()
        print(f"\n❌ Task FAILED:\n{error_detail}")
        send_email(
            subject=f"[Jarvis] ❌ Task '{task_name}' Failed",
            body_html=f"ERROR:\n{str(e)}\n\nFull Traceback:\n{error_detail}",
            success=False
        )
        exit(1)


if __name__ == "__main__":
    main()
