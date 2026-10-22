"""
PROJECT 9 — AutoPilot ⚙️  (Python Automation)
Boring work that takes HOURS by hand → done in SECONDS by Python.

  Task A: Generate personalised certificates for every attendee (from a CSV) → PNG + one combined PDF
  Task B: Clean a messy Downloads folder — sort 100s of files into folders automatically
  Task C: (optional) Email each certificate to its owner via Gmail

Run:  python autopilot.py
"""
import csv
import random
import shutil
import smtplib
import time
from datetime import date
from email.message import EmailMessage
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).parent


def font(size, bold=False):
    names = (["arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"] if bold else ["arial.ttf", "DejaVuSans.ttf", "Arial.ttf"])
    for n in names:
        for folder in ["", "C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/", "/Library/Fonts/", "/System/Library/Fonts/Supplemental/"]:
            try:
                return ImageFont.truetype(folder + n, size)
            except OSError:
                pass
    return ImageFont.load_default(size=size)


# ---------------------------------------------------------------- Task A
def make_sample_csv(path):
    first = ["Arun", "Priya", "Karthik", "Divya", "Vignesh", "Keerthana", "Surya", "Nivetha", "Rahul", "Swetha",
             "Aakash", "Harini", "Gokul", "Lavanya", "Sanjay", "Meena", "Pradeep", "Yamini", "Dinesh", "Janani"]
    last = ["Kumar", "R", "S", "Raj", "M", "Krishnan", "V", "Murugan", "Selvam", "Balaji"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["name", "email", "course"])
        for i in range(50):
            n = f"{random.choice(first)} {random.choice(last)}"
            w.writerow([n, f"{n.split()[0].lower()}{i}@example.com", random.choice(["Full Stack", "Python", "Data Science", "Gen AI"])])


def certificate(name, course, out):
    W, H = 1600, 1130
    img = Image.new("RGB", (W, H), "#0b0b1e")
    d = ImageDraw.Draw(img)
    for i in range(H):  # gradient background
        d.line([(0, i), (W, i)], fill=(11 + i // 40, 11 + i // 60, 30 + i // 18))
    d.rectangle([40, 40, W - 40, H - 40], outline="#ffd23f", width=6)
    d.rectangle([60, 60, W - 60, H - 60], outline="#7c5cff", width=2)
    c = lambda y, text, f, fill: d.text((W / 2, y), text, font=f, fill=fill, anchor="mm")
    c(190, "CERTIFICATE", font(96, True), "#ffd23f")
    c(275, "OF  ACHIEVEMENT", font(40), "#00d4ff")
    c(400, "This is proudly presented to", font(36), "#cfd3ff")
    c(510, name, font(92, True), "#ffffff")
    d.line([(W / 2 - 400, 575), (W / 2 + 400, 575)], fill="#ffd23f", width=3)
    c(660, f"for successfully attending the TechVerse 2026 seminar on", font(34), "#cfd3ff")
    c(730, course, font(58, True), "#2bd67b")
    c(900, date.today().strftime("%d %B %Y"), font(30), "#a3a8c3")
    c(950, "Date", font(24), "#6b6f8f")
    d.ellipse([W - 330, 820, W - 150, 1000], outline="#ffd23f", width=5)
    d.text((W - 240, 910), "VERIFIED", font=font(26, True), fill="#ffd23f", anchor="mm")
    img.save(out)
    return img


def task_certificates():
    data = BASE / "attendees.csv"
    if not data.exists():
        make_sample_csv(data)
        print("   📝 Created sample attendees.csv (50 people) — replace with your real list anytime")
    out = BASE / "certificates"
    out.mkdir(exist_ok=True)
    t = time.time()
    pages = []
    with open(data, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for i, r in enumerate(rows, 1):
        file = out / f"{i:03d}_{r['name'].replace(' ', '_')}.png"
        pages.append(certificate(r["name"], r["course"], file))
        print(f"\r   🖨️  {i}/{len(rows)}  {r['name']:<25}", end="")
    pages[0].save(out / "ALL_CERTIFICATES.pdf", save_all=True, append_images=pages[1:])
    sec = time.time() - t
    print(f"\n   ✅ {len(rows)} certificates + 1 PDF in {sec:.1f} sec  (by hand ≈ {len(rows) * 3} minutes!)")
    print(f"   📂 {out}")


# ---------------------------------------------------------------- Task B
TYPES = {"Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"], "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
         "Videos": [".mp4", ".mkv", ".mov"], "Music": [".mp3", ".wav"], "Code": [".py", ".js", ".html", ".css", ".java"],
         "Archives": [".zip", ".rar", ".7z"], "Installers": [".exe", ".msi", ".apk"]}


def task_organize(folder=None):
    if not folder:
        folder = BASE / "messy_downloads"
        folder.mkdir(exist_ok=True)
        words = ["resume", "IMG_2041", "notes", "project_final_final", "song", "setup", "marksheet", "trip", "assignment", "meme"]
        exts = sum(TYPES.values(), []) + [".xyz"]
        for i in range(120):
            (folder / f"{random.choice(words)}_{i}{random.choice(exts)}").write_text("demo")
        print(f"   🗑️  Created a messy demo folder with 120 random files")
    folder = Path(folder)
    moved = {}
    for f in folder.iterdir():
        if f.is_file():
            kind = next((k for k, v in TYPES.items() if f.suffix.lower() in v), "Others")
            (folder / kind).mkdir(exist_ok=True)
            shutil.move(str(f), folder / kind / f.name)
            moved[kind] = moved.get(kind, 0) + 1
    for k, v in sorted(moved.items(), key=lambda x: -x[1]):
        print(f"   📁 {k:<11} {'■' * (v // 2)} {v}")
    print(f"   ✅ Organised {sum(moved.values())} files in {folder}")


# ---------------------------------------------------------------- Task C
def task_email():
    print("   Uses Gmail + an App Password (Google Account → Security → App passwords)")
    sender = input("   Your Gmail: ").strip()
    pw = input("   App password: ").strip()
    data, out = BASE / "attendees.csv", BASE / "certificates"
    if not sender or not pw or not out.exists():
        return print("   ⚠️ Need Gmail, app password and certificates (run Task A first)")
    dry = input("   Dry run (only print, don't send)? [Y/n]: ").strip().lower() != "n"
    with open(data, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    server = None if dry else smtplib.SMTP_SSL("smtp.gmail.com", 465)
    if server:
        server.login(sender, pw)
    for i, r in enumerate(rows, 1):
        msg = EmailMessage()
        msg["From"], msg["To"], msg["Subject"] = sender, r["email"], "🎉 Your TechVerse 2026 Certificate"
        msg.set_content(f"Hi {r['name']},\n\nThank you for attending! Your certificate is attached.\n\n— Team TechVerse")
        file = out / f"{i:03d}_{r['name'].replace(' ', '_')}.png"
        msg.add_attachment(file.read_bytes(), maintype="image", subtype="png", filename=file.name)
        if server:
            server.send_message(msg)
        print(f"   {'📨 sent' if server else '👀 would send'} → {r['email']}")
    if server:
        server.quit()


if __name__ == "__main__":
    print("\n  ⚙️  AUTOPILOT — Python Automation\n")
    while True:
        print("  A) Generate certificates   B) Organise a messy folder   C) Email certificates   Q) Quit")
        ch = input("  Choose: ").strip().upper()
        if ch == "A": task_certificates()
        elif ch == "B": task_organize(input("   Folder path (Enter = demo folder): ").strip() or None)
        elif ch == "C": task_email()
        elif ch == "Q": break
        print()
