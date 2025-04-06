import { fetchWeatherPage } from './api.js';
import { renderCharts } from './chartRenderer.js';
import { renderPagination } from './pagination.js';

let currentUrl = "http://localhost:8000/api/weather?city=boryspil";

async function initDashboard(url) {
  try {
    const data = await fetchWeatherPage(url);
    renderCharts(data.results);
    renderPagination(data.previous, data.next, initDashboard);
  } catch (err) {
    console.error("Dashboard error:", err);
    document.body.innerHTML += `<p style="color:red;">${err.message}</p>`;
  }
}

initDashboard(currentUrl);
