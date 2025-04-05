async function fetchWeather() {
  const city = document.getElementById("cityInput").value;
  const resultDiv = document.getElementById("weatherResult");

  try {
    const response = await fetch(`http://localhost:8000/api/weather/?city=${city}`);
    if (!response.ok) throw new Error("Weather data not found");

    const data = await response.json();
    resultDiv.innerHTML = `
      <p><strong>City:</strong> ${data.city}</p>
      <p><strong>Temperature:</strong> ${data.temperature}°C</p>
      <p><strong>Description:</strong> ${data.description}</p>
    `;
  } catch (error) {
    resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
  }
}
