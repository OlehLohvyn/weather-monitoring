let currentPageUrl = "http://localhost:8000/api/weather?city=boryspil";

async function drawCharts(url) {
  try {
    const response = await fetch(url, { headers: { 'Accept': 'application/json' } });
    if (!response.ok) throw new Error("Failed to fetch weather data");

    const data = await response.json();
    const weatherEntries = data.results;

    if (!Array.isArray(weatherEntries) || weatherEntries.length === 0) {
      document.body.innerHTML += "<p>No weather data available.</p>";
      return;
    }

    document.getElementById("charts").innerHTML = ""; // очищення перед перемальовуванням

    const labels = weatherEntries.map(e => new Date(e.timestamp).toLocaleTimeString().slice(0, 5));

    const makeDataset = key => weatherEntries.map(e => e[key] ?? null);

    const metrics = [
      { id: "chartTemperature", label: "Temperature (°C)", key: "temperature" },
      { id: "chartFeelsLike", label: "Feels Like (°C)", key: "feels_like" },
      { id: "chartHumidity", label: "Humidity (%)", key: "humidity" },
      { id: "chartPressure", label: "Pressure (mbar)", key: "pressure" },
      { id: "chartDewPoint", label: "Dew Point (°C)", key: "dew_point" },
      { id: "chartPrecipitation", label: "Precipitation (mm)", key: "precipitation" }
    ];

    for (const metric of metrics) {
      const container = document.createElement("div");
      container.className = "chart-container";
      container.innerHTML = `<canvas id="${metric.id}"></canvas>`;
      document.getElementById("charts").appendChild(container);

      new Chart(document.getElementById(metric.id), {
        type: 'line',
        data: {
          labels,
          datasets: [{
            label: metric.label,
            data: makeDataset(metric.key),
            borderWidth: 2,
            fill: false,
            tension: 0.3
          }]
        },
        options: {
          plugins: {
            title: {
              display: true,
              text: metric.label
            }
          },
          scales: {
            x: { title: { display: true, text: "Time" } },
            y: { title: { display: true, text: metric.label }, beginAtZero: false }
          }
        }
      });
    }

    // Кнопки пагінації
    const paginationDiv = document.getElementById("pagination");
    paginationDiv.innerHTML = "";

    if (data.previous) {
      const prevBtn = document.createElement("button");
      prevBtn.innerText = "← Назад";
      prevBtn.onclick = () => drawCharts(data.previous);
      paginationDiv.appendChild(prevBtn);
    }

    if (data.next) {
      const nextBtn = document.createElement("button");
      nextBtn.innerText = "Вперед →";
      nextBtn.onclick = () => drawCharts(data.next);
      paginationDiv.appendChild(nextBtn);
    }

  } catch (error) {
    console.error("ERROR:", error);
    document.body.innerHTML += `<p style="color:red;">${error.message}</p>`;
  }
}

drawCharts(currentPageUrl);
