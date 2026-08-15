(async function(){
  const card  = document.getElementById('weatherCard');
  const icon  = document.getElementById('weatherIconEl');
  const temp  = document.getElementById('weatherTempEl');
  const city  = document.getElementById('weatherCityEl');
  if (!card || !navigator.geolocation) return;

  function weatherEmoji(code){
    if (code === 0)  return '☀️';
    if (code <= 2)   return '⛅';
    if (code <= 3)   return '☁️';
    if (code <= 49)  return '🌫️';
    if (code <= 59)  return '🌦️';
    if (code <= 69)  return '🌧️';
    if (code <= 79)  return '❄️';
    if (code <= 82)  return '🌧️';
    if (code <= 99)  return '⛈️';
    return '🌡️';
  }

  try {
    const pos = await new Promise((res, rej) =>
      navigator.geolocation.getCurrentPosition(res, rej, {timeout: 8000}));
    const {latitude: lat, longitude: lon} = pos.coords;

    const [wRes, gRes] = await Promise.all([
      fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,weather_code&timezone=auto`),
      fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`)
    ]);

    const wData = await wRes.json();
    const gData = await gRes.json();

    const t    = Math.round(wData.current.temperature_2m);
    const code = wData.current.weather_code;
    const addr = gData.address || {};
    const cityName = addr.city || addr.town || addr.village || addr.county || '';

    icon.textContent  = weatherEmoji(code);
    temp.textContent  = `${t}°C`;
    city.textContent  = cityName;
    card.hidden = false;
  } catch(e) {}
})();
