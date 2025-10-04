# راهنمای سطوح دسترسی - TakoTech Website

## **اپ‌های سیستم و مسئولیت‌ها:**

### **1. `accounts` App (اپ اصلی مدیریت کاربران و دسترسی‌ها):**

این اپ **اپ اصلی و پیشرفته** برای مدیریت کاربران، نقش‌ها، گروه‌ها و سطوح دسترسی است.

**مسئولیت‌ها:**
- ✅ **CustomUser Model**: مدل کاربر سفارشی با ویژگی‌های پیشرفته
- ✅ **Role Management**: مدیریت نقش‌ها و مجوزها
- ✅ **MyGroup Management**: مدیریت گروه‌های سفارشی
- ✅ **CustomProfile**: پروفایل کامل کاربر با فیلدهای اضافی
- ✅ **ActiveUser Tracking**: ردیابی کاربران فعال
- ✅ **AuditLog**: ثبت تمام فعالیت‌های سیستم
- ✅ **TimeLock**: قفل زمانی برای امنیت بیشتر
- ✅ **Permission System**: سیستم پیچیده مجوزدهی با PermissionBaseView
- ✅ **Advanced Authentication**: احراز هویت چند مرحله‌ای

**URL Namespace:** `accounts:`

**مثال‌های URL:**
- `/accounts/dashboard/` - داشبورد مدیریت پیشرفته
- `/accounts/users/` - لیست کاربران با فیلترهای پیشرفته
- `/accounts/roles/` - مدیریت نقش‌ها
- `/accounts/groups/` - مدیریت گروه‌ها
- `/accounts/profile/` - پروفایل پیشرفته کاربر

---

### **2. `users` App (اپ ساده برای مدیریت پایه کاربران):**

این اپ برای **مدیریت ساده و پایه کاربران** است که قبل از integrate شدن `accounts` app ایجاد شده بود.

**مسئولیت‌ها:**
- ✅ **Basic User CRUD**: عملیات ساده CRUD برای کاربران
- ✅ **Simple Profile**: پروفایل ساده کاربر
- ✅ **User Preferences**: تنظیمات ساده کاربری
- ✅ **Dashboard**: داشبورد ساده کاربری
- ✅ **APIKey Management**: مدیریت کلیدهای API

**URL Namespace:** `users:`

**مثال‌های URL:**
- `/users/list/` - لیست ساده کاربران
- `/users/dashboard/` - داشبورد ساده کاربری
- `/users/profile/` - پروفایل ساده کاربر
- `/users/preferences/` - تنظیمات کاربری

---

## **🔥 استراتژی پیشنهادی - کدام اپ را استفاده کنیم؟**

### **راه حل 1: استفاده از `accounts` به عنوان اپ اصلی (پیشنهادی ✅)**

این راه حل **بهترین و کامل‌ترین** است:

1. **accounts** = اپ اصلی برای:
   - مدیریت کاربران، نقش‌ها، گروه‌ها
   - سیستم پیچیده مجوزدهی (PermissionBaseView)
   - AuditLog و ردیابی فعالیت‌ها
   - TimeLock و امنیت پیشرفته
   
2. **users** = اپ کمکی برای:
   - CRUD ساده کاربران برای admins
   - APIKey management
   - تنظیمات ساده کاربری

**مزایا:**
- ✅ سیستم پیچیده و کامل مجوزدهی
- ✅ AuditLog کامل برای تمام فعالیت‌ها
- ✅ نقش‌ها و گروه‌های سفارشی
- ✅ امنیت بالاتر با TimeLock

**معایب:**
- ❌ پیچیدگی بیشتر
- ❌ نیاز به یادگیری PermissionBaseView

---

### **راه حل 2: استفاده از `users` به عنوان اپ اصلی**

این راه حل **ساده‌تر** است ولی **محدودتر**:

1. **users** = اپ اصلی برای:
   - CRUD ساده کاربران
   - تنظیمات و پروفایل ساده
   
2. **accounts** = غیرفعال یا حذف

**مزایا:**
- ✅ سادگی بیشتر
- ✅ یادگیری سریع‌تر

**معایب:**
- ❌ فقدان AuditLog
- ❌ عدم وجود نقش‌ها و گروه‌های پیشرفته
- ❌ امنیت کمتر

---

### **راه حل 3: استفاده ترکیبی (موجود در پروژه)**

این راه حل **کنونی** است که **هر دو اپ** استفاده می‌شوند:

1. **accounts** = برای:
   - کاربران پیشرفته با نقش‌ها
   - مدیران ارشد سیستم
   - AuditLog و ردیابی

2. **users** = برای:
   - CRUD ساده کاربران برای admins عادی
   - تنظیمات ساده کاربری
   - APIKey management

**مزایا:**
- ✅ انعطاف‌پذیری بالا
- ✅ هر دو سیستم در دسترس

**معایب:**
- ❌ تداخل احتمالی
- ❌ پیچیدگی در نگهداری

---

## **📌 پیشنهاد نهایی:**

### **برای پروژه TakoTech:**

**استفاده از `accounts` به عنوان اپ اصلی** + **`users` به عنوان اپ کمکی**

**دلایل:**
1. ✅ accounts دارای سیستم پیچیده مجوزدهی است
2. ✅ AuditLog کامل برای تمام فعالیت‌ها
3. ✅ نقش‌ها و گروه‌های سفارشی
4. ✅ TimeLock برای امنیت بالاتر
5. ✅ PermissionBaseView برای کنترل دقیق دسترسی‌ها

**نحوه استفاده:**
- **accounts**: برای تمام عملیات مدیریتی پیشرفته (نقش‌ها، گروه‌ها، AuditLog، TimeLock)
- **users**: فقط برای CRUD ساده کاربران و APIKey management

---

## **⚙️ تنظیمات فعلی:**

```python
# takotech_website/settings.py

AUTH_USER_MODEL = 'accounts.CustomUser'  # ✅ accounts به عنوان اپ اصلی

INSTALLED_APPS = [
    ...
    'accounts.apps.AccountsConfig',  # اپ اصلی
    'users.apps.UsersConfig',  # اپ کمکی
    ...
]
```

---

## **🔐 نحوه استفاده از Permission System:**

### **در `accounts` app:**

```python
from accounts.PermissionBase import PermissionBaseView

class MyView(PermissionBaseView, ListView):
    model = SomeModel
    permission_codename = 'view_somemodel'
    template_name = 'some_template.html'
```

### **در `users` app:**

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class MyView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = SomeModel
    permission_required = 'users.view_somemodel'
    template_name = 'some_template.html'
```

---

## **📊 جدول مقایسه:**

| ویژگی | accounts App | users App |
|-------|-------------|-----------|
| CustomUser Model | ✅ پیشرفته | ❌ ساده (استفاده از accounts.CustomUser) |
| Role Management | ✅ کامل | ❌ ندارد |
| Group Management | ✅ MyGroup | ❌ ندارد |
| AuditLog | ✅ کامل | ❌ ندارد |
| TimeLock | ✅ دارد | ❌ ندارد |
| Permission System | ✅ PermissionBaseView | ❌ Django Default |
| Profile Management | ✅ CustomProfile | ✅ ساده |
| APIKey Management | ❌ ندارد | ✅ دارد |
| Complexity | 🔴 پیچیده | 🟢 ساده |

---

## **✅ نتیجه‌گیری:**

**از این پس:**
1. ✅ **accounts** = اپ اصلی برای مدیریت کاربران، نقش‌ها، گروه‌ها، AuditLog، TimeLock
2. ✅ **users** = اپ کمکی برای CRUD ساده و APIKey management
3. ✅ **AUTH_USER_MODEL** = `accounts.CustomUser`
4. ✅ **Permission System** = `PermissionBaseView` از `accounts.PermissionBase`

---

**تاریخ ایجاد:** 2025-10-04
**نسخه:** 1.0
**وضعیت:** ✅ تایید شده

