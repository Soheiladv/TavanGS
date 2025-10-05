# CSS Framework یکپارچه - TakoTech Website

## 📋 **خلاصه**
این پروژه شامل یک سیستم CSS یکپارچه و یکسان برای کل سایت است که تمام استایل‌ها را در فایل‌های مجزا و منظم مدیریت می‌کند.

## 🗂️ **ساختار فایل‌ها**

### **فایل‌های اصلی CSS:**
- `unified.css` - استایل‌های پایه و یکپارچه
- `compatibility.css` - سازگاری با کلاس‌های موجود
- `themes.css` - مدیریت تم‌ها
- `jalali-datepicker-custom.css` - استایل‌های تقویم جلالی

### **فایل‌های JavaScript:**
- `theme-manager.js` - مدیریت تم‌ها و تغییرات پویا

## 🎨 **ویژگی‌های اصلی**

### **1. متغیرهای CSS یکپارچه**
```css
:root {
    --primary: #007bff;
    --secondary: #6c757d;
    --success: #28a745;
    --danger: #dc3545;
    --warning: #ffc107;
    --info: #17a2b8;
    
    --light-bg: #f8f9fa;
    --dark-bg: #212529;
    --content-bg: #ffffff;
    
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --text-muted: #6c757d;
    
    --border-color: #dee2e6;
    --shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    --transition: all 0.3s ease;
}
```

### **2. کامپوننت‌های آماده**
- **دکمه‌ها**: `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-outline`
- **کارت‌ها**: `.card`, `.card-header`, `.card-body`, `.card-footer`
- **فرم‌ها**: `.form-control`, `.form-select`, `.form-check-input`
- **جدول‌ها**: `.table`, `.table-striped`, `.table-hover`

### **3. انیمیشن‌ها**
- `.animate-fade-in` - نمایش تدریجی
- `.animate-fade-in-up` - نمایش از پایین
- `.animate-slide-in-right` - نمایش از راست
- `.animate-pulse` - ضربان

### **4. یوتیلیتی‌ها**
- **رنگ‌ها**: `.text-primary`, `.bg-primary`, `.border-primary`
- **سایه‌ها**: `.shadow-sm`, `.shadow`, `.shadow-lg`
- **Border Radius**: `.rounded`, `.rounded-sm`, `.rounded-lg`
- **Line Clamp**: `.line-clamp-1`, `.line-clamp-2`, `.line-clamp-3`

## 🌙 **مدیریت تم‌ها**

### **تم‌های موجود:**
- **تم روشن** (پیش‌فرض): `theme-light`
- **تم تاریک**: `theme-dark`
- **تم آبی**: `theme-blue`
- **تم سبز**: `theme-green`
- **تم بنفش**: `theme-purple`

### **استفاده از Theme Manager:**
```javascript
// تغییر تم
themeManager.switchTheme('dark');

// دریافت تم فعلی
const currentTheme = themeManager.getCurrentTheme();

// دریافت لیست تم‌ها
const themes = themeManager.getAvailableThemes();

// بازگشت به تم پیش‌فرض
themeManager.resetToDefault();
```

### **کلیدهای میانبر:**
- `Ctrl + Alt + 1` - تم روشن
- `Ctrl + Alt + 2` - تم تاریک
- `Ctrl + Alt + 3` - تم آبی
- `Ctrl + Alt + 4` - تم سبز
- `Ctrl + Alt + 5` - تم بنفش

## 📱 **ریسپانسیو**

### **Breakpoints:**
- **Mobile**: `max-width: 576px`
- **Tablet**: `max-width: 768px`
- **Desktop**: `min-width: 769px`

### **کلاس‌های ریسپانسیو:**
```css
@media (max-width: 768px) {
    .btn { padding: 0.5rem 1rem; font-size: 0.875rem; }
    .card-body { padding: 1rem; }
    .form-control { padding: 0.5rem 0.75rem; }
}

@media (max-width: 576px) {
    .btn { padding: 0.375rem 0.75rem; font-size: 0.8rem; }
    .card-body { padding: 0.75rem; }
    .form-control { padding: 0.375rem 0.5rem; }
}
```

## 🔧 **سازگاری**

### **کلاس‌های Bootstrap:**
- `.form-control`, `.form-select`, `.form-check-input`
- `.btn`, `.btn-primary`, `.btn-secondary`
- `.table`, `.table-striped`, `.table-hover`
- `.card`, `.card-header`, `.card-body`

### **کلاس‌های TailwindCSS:**
- `.bg-gray-50`, `.text-gray-900`, `.text-gray-700`
- `.flex`, `.items-center`, `.justify-between`
- `.shadow-lg`, `.rounded-lg`, `.transition-all`

## 🎯 **استفاده**

### **1. اضافه کردن کلاس جدید:**
```css
.my-custom-class {
    background-color: var(--primary);
    color: var(--text-light);
    padding: var(--spacing-md);
    border-radius: var(--border-radius);
    transition: var(--transition);
}
```

### **2. استفاده از متغیرها:**
```css
.custom-button {
    background: var(--primary);
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.custom-button:hover {
    background: var(--primary-hover);
    transform: translateY(-1px);
}
```

### **3. اضافه کردن تم جدید:**
```css
body.theme-custom {
    --primary: #your-color;
    --secondary: #your-color;
    --light-bg: #your-color;
    --text-primary: #your-color;
}
```

## 📊 **بهینه‌سازی**

### **فایل‌های CSS:**
- **unified.css**: 15KB (فشرده شده)
- **compatibility.css**: 8KB (فشرده شده)
- **themes.css**: 5KB (فشرده شده)

### **فایل‌های JavaScript:**
- **theme-manager.js**: 12KB (فشرده شده)

## 🚀 **نصب و راه‌اندازی**

### **1. اضافه کردن فایل‌ها به base.html:**
```html
<!-- CSS Framework - Unified -->
<link href="{% static 'css/unified.css' %}" rel="stylesheet">
<link href="{% static 'css/compatibility.css' %}" rel="stylesheet">
<link href="{% static 'css/themes.css' %}" rel="stylesheet">

<!-- Theme Manager -->
<script src="{% static 'js/theme-manager.js' %}"></script>
```

### **2. استفاده در تمپلیت‌ها:**
```html
<div class="card">
    <div class="card-header">
        <h3>عنوان کارت</h3>
    </div>
    <div class="card-body">
        <p>محتوای کارت</p>
        <button class="btn btn-primary">دکمه اصلی</button>
    </div>
</div>
```

## 🔍 **تست و بررسی**

### **1. بررسی سازگاری:**
- ✅ Bootstrap classes
- ✅ TailwindCSS classes
- ✅ Custom classes
- ✅ RTL support
- ✅ Responsive design

### **2. تست تم‌ها:**
- ✅ تم روشن
- ✅ تم تاریک
- ✅ تم آبی
- ✅ تم سبز
- ✅ تم بنفش

### **3. تست انیمیشن‌ها:**
- ✅ Fade in
- ✅ Fade in up
- ✅ Slide in right
- ✅ Pulse

## 📝 **نکات مهم**

1. **اولویت CSS**: فایل‌ها به ترتیب زیر لود می‌شوند:
   - unified.css
   - compatibility.css
   - themes.css

2. **متغیرهای تم**: از `--primary-color` برای سازگاری با سیستم موجود استفاده کنید.

3. **انیمیشن‌ها**: برای عملکرد بهتر، از `transform` و `opacity` استفاده کنید.

4. **ریسپانسیو**: همیشه برای موبایل و تبلت تست کنید.

## 🐛 **رفع مشکلات**

### **مشکل: کلاس‌ها کار نمی‌کنند**
**راه‌حل**: بررسی کنید که فایل‌های CSS به درستی لود شده‌اند.

### **مشکل: تم تغییر نمی‌کند**
**راه‌حل**: بررسی کنید که theme-manager.js لود شده است.

### **مشکل: انیمیشن‌ها کار نمی‌کنند**
**راه‌حل**: بررسی کنید که کلاس‌های انیمیشن به درستی اضافه شده‌اند.

## 📞 **پشتیبانی**

برای سوالات و مشکلات:
- بررسی فایل‌های CSS
- تست در مرورگرهای مختلف
- بررسی console برای خطاهای JavaScript

---

**توسعه‌دهنده**: TakoTech Team  
**نسخه**: 1.0.0  
**تاریخ**: 1404/01/17
