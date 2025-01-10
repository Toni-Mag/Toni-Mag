document.addEventListener('DOMContentLoaded', () => {
    const calendarDisplay = document.getElementById('calendar-display');

    // Празници за 2025 година
    const holidays2025 = {
        "1-1": "New Year's Day",
        "2-14": "Valentine's Day",
        "3-17": "St. Patrick's Day",
        "4-5": "Easter Sunday",
        "5-25": "Memorial Day",
        "7-4": "Independence Day",
        "11-27": "Thanksgiving Day",
        "12-25": "Christmas Day"
    };

    const today = new Date();
    const monthDay = `${today.getMonth() + 1}-${today.getDate()}`;

    // Проверка за днешния празник
    if (holidays2025[monthDay]) {
        calendarDisplay.innerHTML = `<p>Today's Holiday: <strong>${holidays2025[monthDay]}</strong></p>`;
    } else {
        calendarDisplay.innerHTML = `<p>No holidays today.</p>`;
    }

    // Показване на предстоящи празници
    const upcomingHolidays = Object.entries(holidays2025)
        .filter(([date]) => {
            const [month, day] = date.split('-').map(Number);
            const holidayDate = new Date(today.getFullYear(), month - 1, day);
            return holidayDate > today;
        })
        .slice(0, 5);

    if (upcomingHolidays.length > 0) {
        calendarDisplay.innerHTML += '<h4>Upcoming Holidays:</h4><ul>';
        upcomingHolidays.forEach(([date, name]) => {
            calendarDisplay.innerHTML += `<li>${name} (${date})</li>`;
        });
        calendarDisplay.innerHTML += '</ul>';
    }
});

