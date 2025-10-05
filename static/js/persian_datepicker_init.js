// Persian Datepicker Initialization Script
$(document).ready(function() {
    // Function to initialize Persian datepickers
    function initializePersianDatepickers() {
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
                    },
                    onSelect: function(unix) {
                        // Format the selected date
                        const selectedDate = new persianDate(unix);
                        const formattedDate = selectedDate.format('YYYY/MM/DD HH:mm');
                        $(this).val(formattedDate);
                        
                        // Trigger validation
                        $(this).trigger('blur');
                    }
                });
                $(this).addClass('pdatepicker-applied');
            }
        });
    }
    
    // Initialize immediately
    initializePersianDatepickers();
    
    // Re-initialize after any dynamic content is added
    $(document).on('DOMNodeInserted', function() {
        setTimeout(initializePersianDatepickers, 100);
    });
    
    // Also initialize on window load
    $(window).on('load', function() {
        setTimeout(initializePersianDatepickers, 200);
    });
    
    // Initialize when new elements are added dynamically
    $(document).on('click', '.add-row', function() {
        setTimeout(initializePersianDatepickers, 300);
    });
});
