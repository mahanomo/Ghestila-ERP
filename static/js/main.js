let workStart = null;
let logs = [];
let calendarData = [
    { day: "شنبه", note: "جلسه تیمی ساعت ۱۰ صبح" },
    { day: "یک‌شنبه", note: "تحویل پروژه فاز اول" },
    { day: "دوشنبه", note: "آمادگی برای ارائه" },
];

function showSection(id) {
    document.querySelectorAll(".content > div").forEach(div => div.classList.add("hidden"));
    document.getElementById(id).classList.remove("hidden");
}

function startWorkTime() {
    workStart = new Date();
    alert("تایم کاری شروع شد: " + workStart.toLocaleTimeString());
}

function endWorkTime() {
    const report = document.getElementById("daily-report").value;
    if (!report) {
        alert("لطفا قبل از بستن تایم کاری، گزارش کار را ثبت کنید.");
        return;
    }
    const workEnd = new Date();
    const log = {
        start: workStart.toLocaleTimeString(),
        end: workEnd.toLocaleTimeString(),
        report
    };
    logs.push(log);
    updateLogs();
    updateReports();
    workStart = null;
    document.getElementById("daily-report").value = "";
    alert("تایم کاری با موفقیت ثبت شد.");
}

function updateLogs() {
    const list = document.getElementById("log-list");
    list.innerHTML = "";
    logs.forEach((log, index) => {
        list.innerHTML += `<div class="time-log-entry">${index + 1}) از ${log.start} تا ${log.end}</div>`;
    });
}

function updateReports() {
    const list = document.getElementById("report-list");
    list.innerHTML = "";
    logs.forEach((log, index) => {
        list.innerHTML += `<div class="border p-2 my-1 rounded">${index + 1}) ${log.report}</div>`;
    });
}

function showNotification(message) {
    const notification = document.getElementById("notification");
    notification.textContent = message;
    notification.style.display = "block";
    setTimeout(() => {
        notification.style.display = "none";
    }, 4000);
}

function renderCalendar() {
    const container = document.getElementById("calendar-container");
    container.innerHTML = "";
    calendarData.forEach(entry => {
        const note = document.createElement("div");
        note.className = "col-md-3 calendar-day";
        note.innerHTML = `<strong>${entry.day}</strong><div class='calendar-note'>${entry.note}</div>`;
        container.appendChild(note);
        showNotification(`پیام جدید برای ${entry.day}: ${entry.note}`);
    });
}

renderCalendar();