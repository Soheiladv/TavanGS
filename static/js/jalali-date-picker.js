/**
 * Jalali Date Picker JavaScript
 * Handles Jalali date input fields with validation and formatting
 * Integrates with Persian Date Picker library
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Persian Date Pickers
    initializePersianDatePickers();
    
    // Initialize custom Jalali date functionality
    initializeJalaliDateFields();
});

function initializePersianDatePickers() {
    // Initialize Persian date pickers for fields with data-jdp attribute
    if (typeof $ !== 'undefined' && $.fn.pDatepicker) {
        $('[data-jdp]').each(function() {
            if (!$(this).hasClass('pdatepicker-applied')) {
                $(this).pDatepicker({
                    format: 'YYYY/MM/DD HH:mm',
                    autoClose: true,
                    initialValue: false,
                    persianDigit: true,
                    calendar: {
                        persian: {
                            locale: 'fa',
                            showHint: true,
                            leapYearMode: 'algorithmic'
                        }
                    },
                    timePicker: {
                        enabled: true,
                        meridiem: {
                            enabled: false
                        }
                    },
                    checkDate: function(unix) {
                        // Allow all dates
                        return true;
                    }
                });
                $(this).addClass('pdatepicker-applied');
            }
        });
    }
}

function initializeJalaliDateFields() {
    // تنظیم تقویم جلالی برای فیلدهای تاریخ
    const dateFields = document.querySelectorAll('[data-jdp]');
    
    dateFields.forEach(function(field) {
        // تنظیم تقویم جلالی
        field.addEventListener('click', function() {
            // اگر مقدار خالی است، تاریخ فعلی جلالی را تنظیم کن
            if (!this.value) {
                const now = moment();
                const jalaliDate = now.format('jYYYY/jMM/jDD HH:mm');
                this.value = jalaliDate;
            }
        });
        
        // اعتبارسنجی فرمت تاریخ
        field.addEventListener('blur', function() {
            validateJalaliDateField(this);
        });
        
        // اعتبارسنجی در هنگام تایپ
        field.addEventListener('input', function() {
            validateJalaliDateField(this);
        });
        
        // فرمت خودکار هنگام تایپ
        field.addEventListener('keypress', function(e) {
            handleDateInputKeypress(this, e);
        });
        
        // فرمت خودکار هنگام paste
        field.addEventListener('paste', function(e) {
            setTimeout(() => {
                formatJalaliDateField(this);
                validateJalaliDateField(this);
            }, 10);
        });
    });
}

function validateJalaliDateField(field) {
    const value = field.value.trim();
    if (value) {
        // بررسی فرمت تاریخ جلالی
        const dateRegex = /^\d{4}\/\d{1,2}\/\d{1,2}(\s+\d{1,2}:\d{2})?$/;
        if (!dateRegex.test(value)) {
            field.style.borderColor = '#ef4444';
            field.title = 'فرمت تاریخ صحیح نیست. از فرمت 1404/01/17 12:30 استفاده کنید.';
            
            // اضافه کردن کلاس خطا
            field.classList.add('border-red-500');
            field.classList.remove('border-gray-300', 'border-green-500');
        } else {
            field.style.borderColor = '#10b981';
            field.title = '';
            
            // حذف کلاس خطا و اضافه کردن کلاس موفقیت
            field.classList.remove('border-red-500', 'border-gray-300');
            field.classList.add('border-green-500');
        }
    } else {
        // اگر فیلد خالی است، استایل عادی را برگردان
        field.style.borderColor = '#d1d5db';
        field.title = '';
        field.classList.remove('border-red-500', 'border-green-500');
        field.classList.add('border-gray-300');
    }
}

function handleDateInputKeypress(field, e) {
    const value = field.value;
    const cursorPos = field.selectionStart;
    
    // اگر کاربر اسلش تایپ کرد، بررسی کن که آیا در جای درست است
    if (e.key === '/') {
        const parts = value.substring(0, cursorPos).split('/');
        if (parts.length >= 3) {
            e.preventDefault();
            return false;
        }
    }
    
    // اگر کاربر دو نقطه تایپ کرد، بررسی کن که آیا در جای درست است
    if (e.key === ':') {
        const timePart = value.split(' ')[1];
        if (timePart && timePart.includes(':')) {
            e.preventDefault();
            return false;
        }
    }
}

function formatJalaliDateField(field) {
    let value = field.value.trim();
    
    // حذف کاراکترهای غیرضروری
    value = value.replace(/[^\d\/\s:]/g, '');
    
    // فرمت تاریخ
    value = formatJalaliDate(value);
    
    field.value = value;
}

// تابع فرمت کردن تاریخ جلالی
function formatJalaliDate(value) {
    // حذف فاصله‌های اضافی
    value = value.replace(/\s+/g, ' ').trim();
    
    // تقسیم به بخش‌های تاریخ و زمان
    const parts = value.split(' ');
    let datePart = parts[0];
    let timePart = parts[1] || '';
    
    // فرمت بخش تاریخ
    if (datePart) {
        const dateNumbers = datePart.replace(/\D/g, '');
        if (dateNumbers.length >= 4) {
            let formatted = dateNumbers.substring(0, 4);
            if (dateNumbers.length >= 6) {
                formatted += '/' + dateNumbers.substring(4, 6);
            }
            if (dateNumbers.length >= 8) {
                formatted += '/' + dateNumbers.substring(6, 8);
            }
            datePart = formatted;
        }
    }
    
    // فرمت بخش زمان
    if (timePart) {
        const timeNumbers = timePart.replace(/\D/g, '');
        if (timeNumbers.length >= 2) {
            let formatted = timeNumbers.substring(0, 2);
            if (timeNumbers.length >= 4) {
                formatted += ':' + timeNumbers.substring(2, 4);
            }
            timePart = formatted;
        }
    }
    
    // ترکیب نهایی
    if (timePart) {
        return datePart + ' ' + timePart;
    }
    return datePart;
}

// تابع اعتبارسنجی تاریخ جلالی
function validateJalaliDate(dateString) {
    if (!dateString) return true;
    
    const regex = /^\d{4}\/\d{1,2}\/\d{1,2}(\s+\d{1,2}:\d{2})?$/;
    if (!regex.test(dateString)) return false;
    
    try {
        const parts = dateString.split(' ');
        const datePart = parts[0];
        const timePart = parts[1] || '00:00';
        
        const [year, month, day] = datePart.split('/').map(Number);
        const [hour, minute] = timePart.split(':').map(Number);
        
        // بررسی محدوده‌های معتبر
        if (year < 1300 || year > 1500) return false;
        if (month < 1 || month > 12) return false;
        if (day < 1 || day > 31) return false;
        if (hour < 0 || hour > 23) return false;
        if (minute < 0 || minute > 59) return false;
        
        return true;
    } catch (e) {
        return false;
    }
}

// تابع کمکی برای تنظیم تاریخ فعلی جلالی
function setCurrentJalaliDate(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        const now = moment();
        const jalaliDate = now.format('jYYYY/jMM/jDD HH:mm');
        field.value = jalaliDate;
        validateJalaliDateField(field);
    }
}

// تابع کمکی برای پاک کردن فیلد تاریخ
function clearJalaliDate(fieldId) {
    const field = document.getElementById(fieldId);
    if (field) {
        field.value = '';
        field.style.borderColor = '#d1d5db';
        field.title = '';
        field.classList.remove('border-red-500', 'border-green-500');
        field.classList.add('border-gray-300');
    }
}

// اضافه کردن توابع به window برای استفاده در جاهای دیگر
window.validateJalaliDate = validateJalaliDate;
window.formatJalaliDate = formatJalaliDate;
window.setCurrentJalaliDate = setCurrentJalaliDate;
window.clearJalaliDate = clearJalaliDate;
window.initializePersianDatePickers = initializePersianDatePickers;
