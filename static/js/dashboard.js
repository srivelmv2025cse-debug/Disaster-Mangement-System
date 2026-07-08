/* ============================================
   DASHBOARD.JS – Core utility functions
   ============================================ */

// Toggle sidebar on mobile
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// Loading overlay
function showLoading(show) {
  const el = document.getElementById('loadingOverlay');
  if (show) el.classList.add('show');
  else el.classList.remove('show');
}

// Live clock
function updateClock() {
  const now = new Date();
  const str = now.toLocaleString('en-US', {
    weekday: 'short', year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
  const el = document.getElementById('topbar-clock');
  if (el) el.textContent = str;
}
setInterval(updateClock, 1000);
updateClock();

// CSRF helper
function getCookie(name) {
  let val = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(c => {
      c = c.trim();
      if (c.startsWith(name + '=')) {
        val = decodeURIComponent(c.substring(name.length + 1));
      }
    });
  }
  return val;
}

// Animate number counting
function animateValue(id, end, duration = 1200) {
  const el = document.getElementById(id);
  if (!el) return;
  const start = 0;
  const endNum = parseInt(end) || 0;
  if (endNum === 0) { el.textContent = '0'; return; }
  let startTime = null;
  function step(timestamp) {
    if (!startTime) startTime = timestamp;
    const progress = Math.min((timestamp - startTime) / duration, 1);
    el.textContent = Math.floor(progress * endNum).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = endNum.toLocaleString();
  }
  requestAnimationFrame(step);
}

// Populate home summary cards
function populateSummaryCards(s) {
  if (!s) return;
  animateValue('val-total', s.total_records);
  document.getElementById('val-temp').textContent = s.avg_temperature + '°C';
  document.getElementById('val-rain').textContent = s.total_rainfall + ' mm';
  animateValue('val-risk', s.high_risk_alerts);
  animateValue('val-critical', s.critical_disaster_count);
  document.getElementById('val-city').textContent = s.most_affected_city;
  document.getElementById('val-wind').textContent = s.avg_wind_speed + ' km/h';
  document.getElementById('val-hum').textContent = s.avg_humidity + '%';

  // Remove loading state
  document.querySelectorAll('.loading-card').forEach(c => c.classList.remove('loading-card'));
}
