document.addEventListener("DOMContentLoaded", function () {
  const subjectSelect = document.getElementById("subject");
  const progressInput = document.getElementById("progress");
  const progressForm = document.getElementById("progressForm");
  const studyBtn = document.getElementById("studyBtn");
  const streakDisplay = document.getElementById("streakDisplay");

  // Populate subject dropdown
  const subjects = Object.keys(progressData).filter(s => s !== "streaks");
  subjects.forEach(subject => {
    const option = document.createElement("option");
    option.value = subject;
    option.textContent = subject;
    subjectSelect.appendChild(option);
  });

  // Radar chart
  const radarCtx = document.getElementById("radarChart").getContext("2d");
  const radarChart = new Chart(radarCtx, {
    type: "radar",
    data: {
      labels: subjects,
      datasets: [{
        label: "Progress %",
        data: subjects.map(sub => progressData[sub]),
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        r: {
          angleLines: { display: false },
          suggestedMin: 0,
          suggestedMax: 100
        }
      }
    }
  });

  // Update progress
  progressForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const subject = subjectSelect.value;
    const progress = parseInt(progressInput.value);

    fetch("/update", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: `subject=${subject}&progress=${progress}`
    })
    .then(res => res.json())
    .then(() => location.reload());
  });

  // Mark study streak
  studyBtn.addEventListener("click", function () {
    fetch("/mark_study", {
      method: "POST"
    })
    .then(res => res.json())
    .then(() => location.reload());
  });

  // Display streaks
  const streakDates = progressData.streaks || [];
  streakDisplay.innerHTML = streakDates.length
    ? `<p>You’ve studied on ${streakDates.length} day(s) 🎉</p>`
    : `<p>No study streaks yet.</p>`;
});
