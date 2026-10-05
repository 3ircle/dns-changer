# 🌐 dns-changer

> ابزاری ساده و سریع برای **تغییر، مدیریت و پاک‌سازی DNS** در ویندوز — فقط با یک دستور.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)]()

---

## 📖 درباره پروژه

`dns-changer` یک اسکریپت خط‌فرمانی پایتون است که به شما اجازه می‌دهد بدون گشتن در تنظیمات ویندوز، **DNS** سیستم را تنها با یک دستور عوض کنید. این ابزار:

- آداپتور شبکه فعال را **خودکار** پیدا می‌کند.
- مجموعه‌ای از DNSهای پرکاربرد را در `dns-list.json` نگه می‌دارد.
- در صورت نیاز، خودش را با **دسترسی ادمین (UAC)** دوباره اجرا می‌کند.
- از دستور بومی `netsh` ویندوز برای اعمال تنظیمات استفاده می‌کند.

---

## ⚡ شروع سریع

```bash
# ۱. کلون مخزن
git clone <repository-url>
cd dns-changer

# ۲. نصب وابستگی
pip install -r requirements.txt

# ۳. مشاهده لیست DNSهای آماده
python dns-changer.py -list

# ۴. تغییر DNS به Shecan
python dns-changer.py -set shecan
```

> 💡 در اجرای اول یک پنجره **UAC** ظاهر می‌شود؛ این طبیعی است و برای دسترسی ادمین لازم است.

---

## 🧰 پیش‌نیازها

| مورد | نسخه |
|------|------|
| ویندوز | 10 / 11 |
| پایتون | 3.8 یا بالاتر |
| دسترسی | Administrator |

تنها وابستگی خارجی: **`psutil`** (در `requirements.txt` تعریف شده).

---

## 🚀 راهنمای استفاده

### 1️⃣ تنظیم DNS — `-set`

**با آدرس IP مستقیم:**

```bash
python dns-changer.py -set 8.8.8.8
python dns-changer.py -set 8.8.8.8 8.8.4.4
```

- آرگومان دوم → DNS اصلی
- آرگومان سوم (اختیاری) → DNS ثانویه

**با نام DNS ذخیره‌شده:**

```bash
python dns-changer.py -set shecan
python dns-changer.py -set google
python dns-changer.py -set electro
```

---

### 2️⃣ پاک‌سازی DNS — `-clear`

DNS آداپتور فعال را به حالت **خودکار (DHCP)** برمی‌گرداند:

```bash
python dns-changer.py -clear
```

خروجی:

```
DNS for 'Ethernet' reset to automatic (DHCP)
```

---

### 3️⃣ افزودن DNS جدید — `-add`

```bash
# فقط DNS اصلی
python dns-changer.py -add <name> <primary>

# با DNS ثانویه
python dns-changer.py -add <name> <primary> <secondary>
```

مثال:

```bash
python dns-changer.py -add cloudflare 1.1.1.1 1.0.0.1
```

سپس:

```bash
python dns-changer.py -set cloudflare
```

---

### 4️⃣ نمایش لیست DNSها — `-list`

```bash
python dns-changer.py -list
```

خروجی نمونه:

```
[shecan][178.22.122.100][185.51.200.2]
[electro][78.157.42.100][78.157.42.101]
[google][8.8.8.8][None]
```

> 🔸 `[None]` یعنی برای آن DNS، آدرس ثانویه ثبت نشده است.

---

## 🖱️ اجرا با دابل‌کلیک (اختیاری)

به‌جای تایپ دستور، می‌توانید از فایل `dns.bat` استفاده کنید:

```bat
dns.bat -list
dns.bat -set shecan
dns.bat -clear
```

---

## 📋 دستورات به‌طور خلاصه

| دستور | توضیح | مثال |
|-------|-------|------|
| `-set <ip> [ip2]` | تنظیم DNS با آدرس IP | `-set 8.8.8.8 8.8.4.4` |
| `-set <name>` | تنظیم DNS با نام ذخیره‌شده | `-set shecan` |
| `-clear` | بازگرداندن DNS به DHCP | `-clear` |
| `-add <name> <ip> [ip2]` | افزودن DNS جدید | `-add cf 1.1.1.1` |
| `-list` | نمایش همه DNSهای ذخیره‌شده | `-list` |

---

## 📁 ساختار پروژه

```
dns-changer/
├── dns-changer.py      # اسکریپت اصلی
├── dns-list.json       # دیتابیس DNSهای ذخیره‌شده
├── dns.bat             # لانچر ویندوزی
├── requirements.txt    # وابستگی‌ها
├── README.md           # همین فایل
├── DOCUMENTATION.md    # مستندات کامل
└── LICENSE             # مجوز MIT
```

---

## 🗂️ فرمت dns-list.json

```json
[
  { "shecan":  ["178.22.122.100", "185.51.200.2"] },
  { "google":  ["8.8.8.8", null] }
]
```

هر شیء یک جفت **نام → [primary, secondary]** است. اگر DNS ثانویه نداشته باشد، `null` قرار دهید.

---

## ❓ عیب‌یابی

| مشکل | راه‌حل |
|------|-------|
| `ModuleNotFoundError: psutil` | `pip install -r requirements.txt` |
| `no active network adapter found` | اتصال شبکه را بررسی کنید |
| `dns is not valid` | آدرس باید `x.x.x.x` معتبر باشد |
| `dns alredy exist` | نام تکراری است؛ نام دیگری بدهید |
| پنجره UAC ظاهر نمی‌شود | برنامه را مستقیم با Run as Administrator اجرا کنید |

---

## ⚠️ محدودیت‌ها

- فقط **ویندوز** و **IPv4** پشتیبانی می‌شود (IPv6 ندارد).
- در سیستم‌های دارای چند آداپتور مجازی (VPN/WSL/Hyper-V)، ممکن است آداپتور اشتباه انتخاب شود.
- اعتبارسنجی IP فقط عددی بودن بخش‌ها را چک می‌کند (بازه 0-255 به‌طور کامل چک نمی‌شود).

---

## 📄 مستندات بیشتر

برای توضیحات کامل‌تر (نحوه کار داخلی، توسعه، جزئیات فنی) فایل [`DOCUMENTATION.md`](DOCUMENTATION.md) را ببینید.

---

## 📜 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است. جزئیات در فایل [LICENSE](LICENSE).
