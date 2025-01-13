document.addEventListener('DOMContentLoaded', () => {
    const calendarDisplay = document.getElementById('calendar-display');

    // Празници и банкови празници за 2025 година
    const holidays2025 = {
        "1-1": "New Year's Day",
        "3-17": "St. Patrick's Day (Northern Ireland)",
        "4-18": "Good Friday",
        "4-21": "Easter Monday",
        "5-5": "Early May Bank Holiday",
        "5-26": "Spring Bank Holiday",
        "7-12": "Battle of the Boyne (Northern Ireland)",
        "8-25": "Summer Bank Holiday",
        "11-5": "Guy Fawkes Night",
        "12-25": "Christmas Day",
        "12-26": "Boxing Day"
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
        .sort(([dateA], [dateB]) => {
            const [monthA, dayA] = dateA.split('-').map(Number);
            const [monthB, dayB] = dateB.split('-').map(Number);
            return new Date(today.getFullYear(), monthA - 1, dayA) - new Date(today.getFullYear(), monthB - 1, dayB);
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

