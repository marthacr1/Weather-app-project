const cityInput = document.getElementById("cityInput");
const searchBtn = document.getElementById("searchBtn");
const errorMsg  = document.getElementById("error-msg");
const currentSection  = document.getElementById("current-weather");
const forecastSection = document.getElementById("forecast-section");

function showError(msg) {
  errorMsg.textContent = msg;
  errorMsg.classList.remove("hidden");
  currentSection.classList.add("hidden");
  forecastSection.classList.add("hidden");
}

function clearError() {
  errorMsg.classList.add("hidden");
}

function iconUrl(code) {
  return `https://openweathermap.org/img/wn/${code}@2x.png`;
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { weekday: "short", month: "short", day: "numeric" });
}

async function fetchWeather(city) {
  searchBtn.classList.add("loading");
  searchBtn.textContent = "Loading…";
  clearError();

  try {
    const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
    const data = await res.json();

    if (!res.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    // --- current ---
    document.getElementById("city-name").textContent   = `${data.city}, ${data.country}`;
    document.getElementById("weather-desc").textContent = data.current.description;
    document.getElementById("current-temp").textContent = `${data.current.temp}°C`;
    document.getElementById("weather-icon").src         = iconUrl(data.current.icon);
    document.getElementById("feels-like").textContent   = `${data.current.feels_like}°C`;
    document.getElementById("humidity").textContent     = `${data.current.humidity}%`;
    document.getElementById("wind").textContent         = `${data.current.wind_speed} m/s`;
    document.getElementById("visibility").textContent   = `${data.current.visibility} km`;
    document.getElementById("pressure").textContent     = `${data.current.pressure} hPa`;

    currentSection.classList.remove("hidden");

    // --- forecast ---
    const grid = document.getElementById("forecast-cards");
    grid.innerHTML = "";
    data.forecast.forEach((day, i) => {
      const card = document.createElement("div");
      card.className = "forecast-card";
      card.style.animationDelay = `${i * 0.07}s`;
      card.innerHTML = `
        <p class="forecast-date">${formatDate(day.date)}</p>
        <img src="${iconUrl(day.icon)}" alt="${day.description}" />
        <p class="forecast-desc">${day.description}</p>
        <p class="forecast-temps">
          <span class="temp-max">${day.temp_max}°</span>
          <span class="temp-min">${day.temp_min}°</span>
        </p>`;
      grid.appendChild(card);
    });

    forecastSection.classList.remove("hidden");
  } catch (err) {
    showError("Network error — please try again.");
  } finally {
    searchBtn.classList.remove("loading");
    searchBtn.textContent = "Search";
  }
}

searchBtn.addEventListener("click", () => {
  const city = cityInput.value.trim();
  if (city) fetchWeather(city);
});

cityInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const city = cityInput.value.trim();
    if (city) fetchWeather(city);
  }
});
