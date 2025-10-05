/* ================================================== */
/* === Theme Management JavaScript === */
/* === مدیریت تم‌ها و تغییرات پویا === */
/* ================================================== */

class ThemeManager {
    constructor() {
        this.currentTheme = this.getStoredTheme() || 'light';
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createThemeSwitcher();
        this.bindEvents();
    }

    getStoredTheme() {
        return localStorage.getItem('theme');
    }

    setStoredTheme(theme) {
        localStorage.setItem('theme', theme);
    }

    applyTheme(theme) {
        // حذف کلاس‌های تم قبلی
        document.body.classList.remove('theme-light', 'theme-dark', 'theme-blue', 'theme-green', 'theme-purple');
        
        // اضافه کردن کلاس تم جدید
        document.body.classList.add(`theme-${theme}`);
        
        // ذخیره تم در localStorage
        this.setStoredTheme(theme);
        
        // به‌روزرسانی متغیرهای CSS
        this.updateCSSVariables(theme);
        
        // اطلاع‌رسانی تغییر تم
        this.notifyThemeChange(theme);
    }

    updateCSSVariables(theme) {
        const root = document.documentElement;
        
        // تنظیم متغیرهای تم بر اساس تم انتخاب شده
        switch(theme) {
            case 'light':
                root.style.setProperty('--primary-color', '#007bff');
                root.style.setProperty('--secondary-color', '#6c757d');
                root.style.setProperty('--accent-color', '#17a2b8');
                break;
            case 'dark':
                root.style.setProperty('--primary-color', '#0d6efd');
                root.style.setProperty('--secondary-color', '#6c757d');
                root.style.setProperty('--accent-color', '#0dcaf0');
                break;
            case 'blue':
                root.style.setProperty('--primary-color', '#3498db');
                root.style.setProperty('--secondary-color', '#95a5a6');
                root.style.setProperty('--accent-color', '#1abc9c');
                break;
            case 'green':
                root.style.setProperty('--primary-color', '#4caf50');
                root.style.setProperty('--secondary-color', '#9e9e9e');
                root.style.setProperty('--accent-color', '#00bcd4');
                break;
            case 'purple':
                root.style.setProperty('--primary-color', '#9c27b0');
                root.style.setProperty('--secondary-color', '#9e9e9e');
                root.style.setProperty('--accent-color', '#00bcd4');
                break;
        }
    }

    createThemeSwitcher() {
        // بررسی وجود theme switcher
        if (document.getElementById('theme-switcher')) {
            return;
        }

        const switcher = document.createElement('div');
        switcher.id = 'theme-switcher';
        switcher.className = 'theme-switcher';
        switcher.innerHTML = `
            <button class="theme-light" title="تم روشن" data-theme="light"></button>
            <button class="theme-dark" title="تم تاریک" data-theme="dark"></button>
            <button class="theme-blue" title="تم آبی" data-theme="blue"></button>
            <button class="theme-green" title="تم سبز" data-theme="green"></button>
            <button class="theme-purple" title="تم بنفش" data-theme="purple"></button>
        `;

        document.body.appendChild(switcher);
    }

    bindEvents() {
        // رویداد تغییر تم
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-theme]')) {
                const theme = e.target.getAttribute('data-theme');
                this.switchTheme(theme);
            }
        });

        // رویداد تغییر تم از طریق کلیدهای میانبر
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.altKey) {
                switch(e.key) {
                    case '1':
                        e.preventDefault();
                        this.switchTheme('light');
                        break;
                    case '2':
                        e.preventDefault();
                        this.switchTheme('dark');
                        break;
                    case '3':
                        e.preventDefault();
                        this.switchTheme('blue');
                        break;
                    case '4':
                        e.preventDefault();
                        this.switchTheme('green');
                        break;
                    case '5':
                        e.preventDefault();
                        this.switchTheme('purple');
                        break;
                }
            }
        });
    }

    switchTheme(theme) {
        if (this.currentTheme !== theme) {
            this.currentTheme = theme;
            this.applyTheme(theme);
            
            // نمایش پیام تغییر تم
            this.showNotification(`تم به ${this.getThemeName(theme)} تغییر یافت`);
        }
    }

    getThemeName(theme) {
        const names = {
            'light': 'روشن',
            'dark': 'تاریک',
            'blue': 'آبی',
            'green': 'سبز',
            'purple': 'بنفش'
        };
        return names[theme] || theme;
    }

    showNotification(message) {
        // حذف notification قبلی
        const existingNotification = document.getElementById('theme-notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.id = 'theme-notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--primary);
            color: var(--text-light);
            padding: 12px 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            z-index: 10000;
            font-family: var(--font-primary);
            font-size: 14px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        notification.textContent = message;

        document.body.appendChild(notification);

        // انیمیشن نمایش
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 100);

        // حذف خودکار بعد از 3 ثانیه
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }

    notifyThemeChange(theme) {
        // ارسال رویداد تغییر تم
        const event = new CustomEvent('themeChanged', {
            detail: {
                theme: theme,
                themeName: this.getThemeName(theme)
            }
        });
        document.dispatchEvent(event);
    }

    // متدهای عمومی
    getCurrentTheme() {
        return this.currentTheme;
    }

    getAvailableThemes() {
        return ['light', 'dark', 'blue', 'green', 'purple'];
    }

    resetToDefault() {
        this.switchTheme('light');
    }
}

// ایجاد instance از ThemeManager
const themeManager = new ThemeManager();

// در دسترس قرار دادن در window برای استفاده در سایر اسکریپت‌ها
window.themeManager = themeManager;

// رویداد تغییر تم
document.addEventListener('themeChanged', (e) => {
    console.log('تم تغییر یافت:', e.detail.themeName);
    
    // به‌روزرسانی عناصر خاص در صورت نیاز
    updateThemeSpecificElements(e.detail.theme);
});

function updateThemeSpecificElements(theme) {
    // به‌روزرسانی عناصر خاص بر اساس تم
    const elements = document.querySelectorAll('[data-theme-specific]');
    elements.forEach(element => {
        const themeSpecificClass = element.getAttribute('data-theme-specific');
        if (themeSpecificClass) {
            element.className = element.className.replace(/theme-\w+/g, '');
            element.classList.add(`theme-${theme}`);
        }
    });
}

// سازگاری با سیستم تم موجود
if (typeof window !== 'undefined') {
    // بررسی وجود سیستم تم قبلی
    if (window.themeSystem) {
        // ادغام با سیستم تم موجود
        window.themeSystem = Object.assign(window.themeSystem, themeManager);
    } else {
        // ایجاد سیستم تم جدید
        window.themeSystem = themeManager;
    }
}

// export برای استفاده در ماژول‌ها
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
