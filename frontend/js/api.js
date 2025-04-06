export async function fetchWeatherPage(url) {
    const res = await fetch(url, {
      headers: { 'Accept': 'application/json' }
    });
  
    if (!res.ok) throw new Error("API request failed");
  
    return await res.json();
  }
  