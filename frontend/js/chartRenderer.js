export function renderCharts(entries) {
    document.getElementById("charts").innerHTML = "";
  
    const labels = entries.map(e => new Date(e.timestamp).toLocaleTimeString().slice(0, 5));
  
    const getData = key => entries.map(e => e[key] ?? null);
  
    const metrics = [
      { id: "chartTemperature", label: "Temperature (°C)", key: "temperature" },
      { id: "chartFeelsLike", label: "Feels Like (°C)", key: "feels_like" },
      { id: "chartHumidity", label: "Humidity (%)", key: "humidity" },
      { id: "chartPressure", label: "Pressure (mbar)", key: "pressure" },
      { id: "chartDewPoint", label: "Dew Point (°C)", key: "dew_point" },
      { id: "chartPrecipitation", label: "Precipitation (mm)", key: "precipitation" },
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
            data: getData(metric.key),
            borderWidth: 2,
            fill: false,
            tension: 0.3
          }]
        },
        options: {
          plugins: { title: { display: true, text: metric.label } },
          scales: {
            x: { title: { display: true, text: "Time" } },
            y: { title: { display: true, text: metric.label }, beginAtZero: false }
          }
        }
      });
    }
  }
  