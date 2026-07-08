/* ============================================
   CHARTS.JS – Chart.js & Plotly Renderers
   ============================================ */

const CHART_COLORS = {
  blue:   '#4e8cff',
  cyan:   '#22d3ee',
  purple: '#a855f7',
  pink:   '#f472b6',
  green:  '#34d399',
  orange: '#fb923c',
  red:    '#ef4444',
  yellow: '#facc15',
};

const PALETTE = [
  CHART_COLORS.blue, CHART_COLORS.cyan, CHART_COLORS.purple,
  CHART_COLORS.pink, CHART_COLORS.green, CHART_COLORS.orange,
  CHART_COLORS.red,  CHART_COLORS.yellow
];

const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

// Global defaults
Chart.defaults.color = 'rgba(232,234,246,0.55)';
Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';
Chart.defaults.font.family = "'Outfit', sans-serif";

// Helper – destroy existing chart on canvas
function safeDestroy(id) {
  const existing = Chart.getChart(id);
  if (existing) existing.destroy();
}

// ── LINE CHART ────────────────────────────────────
function renderLineChart(canvasId, dataObj, label) {
  safeDestroy(canvasId);
  const keys = Object.keys(dataObj).sort((a,b) => Number(a)-Number(b));
  const labels = keys.map(k => MONTH_NAMES[Number(k)-1] || k);
  const values = keys.map(k => dataObj[k]);

  return new Chart(document.getElementById(canvasId).getContext('2d'), {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label,
        data: values,
        borderColor: CHART_COLORS.cyan,
        backgroundColor: 'rgba(34,211,238,0.08)',
        borderWidth: 2.5,
        pointBackgroundColor: CHART_COLORS.cyan,
        pointRadius: 4,
        pointHoverRadius: 7,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false }, tooltip: { mode: 'index' } },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' } }
      },
      animation: { duration: 900, easing: 'easeInOutQuart' }
    }
  });
}

// ── BAR CHART ─────────────────────────────────────
function renderBarChart(canvasId, dataObj, label) {
  safeDestroy(canvasId);
  const keys = Object.keys(dataObj);
  const values = keys.map(k => dataObj[k]);
  const colors = keys.map((_, i) => PALETTE[i % PALETTE.length]);

  return new Chart(document.getElementById(canvasId).getContext('2d'), {
    type: 'bar',
    data: {
      labels: keys,
      datasets: [{
        label,
        data: values,
        backgroundColor: colors.map(c => c + 'aa'),
        borderColor: colors,
        borderWidth: 1.5,
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { maxRotation: 30, font: { size: 11 } } },
        y: { grid: { color: 'rgba(255,255,255,0.04)' } }
      },
      animation: { duration: 900, easing: 'easeOutBounce' }
    }
  });
}

// ── PIE CHART ─────────────────────────────────────
function renderPieChart(canvasId, dataObj, label) {
  safeDestroy(canvasId);
  const keys = Object.keys(dataObj);
  const values = keys.map(k => dataObj[k]);

  return new Chart(document.getElementById(canvasId).getContext('2d'), {
    type: 'pie',
    data: {
      labels: keys,
      datasets: [{
        data: values,
        backgroundColor: PALETTE.map(c => c + 'cc'),
        borderColor: PALETTE,
        borderWidth: 1.5
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, padding: 12, font: { size: 11 } } }
      },
      animation: { duration: 1000, animateRotate: true }
    }
  });
}

// ── DONUT CHART ───────────────────────────────────
function renderDonutChart(canvasId, dataObj, label) {
  safeDestroy(canvasId);
  const riskColors = {
    Low:      CHART_COLORS.green,
    Medium:   CHART_COLORS.yellow,
    High:     CHART_COLORS.orange,
    Critical: CHART_COLORS.red
  };
  const keys = Object.keys(dataObj);
  const values = keys.map(k => dataObj[k]);
  const colors = keys.map(k => riskColors[k] || CHART_COLORS.blue);

  return new Chart(document.getElementById(canvasId).getContext('2d'), {
    type: 'doughnut',
    data: {
      labels: keys,
      datasets: [{
        data: values,
        backgroundColor: colors.map(c => c + 'bb'),
        borderColor: colors,
        borderWidth: 2,
        hoverOffset: 8
      }]
    },
    options: {
      responsive: true,
      cutout: '65%',
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, padding: 10, font: { size: 11 } } }
      },
      animation: { duration: 900, animateRotate: true }
    }
  });
}

// ── SCATTER PLOT (Plotly) ─────────────────────────
function renderScatterPlotly(divId, scatterData) {
  if (!scatterData || scatterData.length === 0) return;
  const x = scatterData.map(d => d.rainfall);
  const y = scatterData.map(d => d.river_level);

  const trace = {
    x, y,
    mode: 'markers',
    type: 'scatter',
    marker: {
      color: CHART_COLORS.cyan,
      size: 7,
      opacity: 0.7,
      line: { color: CHART_COLORS.blue, width: 0.5 }
    },
    name: 'Rainfall vs River Level'
  };

  const layout = {
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'transparent',
    font: { family: "'Outfit', sans-serif", color: 'rgba(232,234,246,0.6)', size: 11 },
    xaxis: { title: 'Rainfall (mm)', gridcolor: 'rgba(255,255,255,0.04)', zerolinecolor: 'rgba(255,255,255,0.08)' },
    yaxis: { title: 'River Level (m)',  gridcolor: 'rgba(255,255,255,0.04)', zerolinecolor: 'rgba(255,255,255,0.08)' },
    margin: { t: 10, l: 50, r: 10, b: 50 },
    showlegend: false
  };

  Plotly.newPlot(divId, [trace], layout, { responsive: true, displayModeBar: false });
}

// ── 24-HOUR FORECAST CHART ────────────────────────
function renderForecastChart(forecast) {
  safeDestroy('forecastChart');
  const labels = forecast.times.map(t => {
    const d = new Date(t);
    return d.getHours() + ':00';
  });

  new Chart(document.getElementById('forecastChart').getContext('2d'), {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Temperature (°C)',
          data: forecast.temperatures,
          borderColor: CHART_COLORS.orange,
          backgroundColor: 'rgba(251,146,60,0.1)',
          borderWidth: 2.5,
          yAxisID: 'y',
          fill: true,
          tension: 0.4,
          pointRadius: 3
        },
        {
          label: 'Humidity (%)',
          data: forecast.humidities,
          borderColor: CHART_COLORS.blue,
          backgroundColor: 'rgba(78,140,255,0.08)',
          borderWidth: 2,
          yAxisID: 'y1',
          fill: false,
          tension: 0.4,
          pointRadius: 2,
          borderDash: [5, 3]
        },
        {
          label: 'Wind Speed (km/h)',
          data: forecast.wind_speeds,
          borderColor: CHART_COLORS.green,
          backgroundColor: 'transparent',
          borderWidth: 2,
          yAxisID: 'y1',
          fill: false,
          tension: 0.4,
          pointRadius: 2,
          borderDash: [3, 3]
        }
      ]
    },
    options: {
      responsive: true,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'top', labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: { mode: 'index' }
      },
      scales: {
        x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { maxTicksLimit: 12 } },
        y: {
          type: 'linear', position: 'left',
          grid: { color: 'rgba(255,255,255,0.04)' },
          title: { display: true, text: '°C', color: CHART_COLORS.orange }
        },
        y1: {
          type: 'linear', position: 'right',
          grid: { drawOnChartArea: false },
          title: { display: true, text: '% / km/h', color: CHART_COLORS.blue }
        }
      },
      animation: { duration: 1000, easing: 'easeInOutQuart' }
    }
  });
}

// ── RENDER ALL HOME CHARTS ────────────────────────
function renderAllHomeCharts(c) {
  if (!c) return;
  renderLineChart('monthlyTempChart', c.monthly_temp, 'Avg Temperature (°C)');
  renderBarChart('cityRainfallChart', c.city_rainfall, 'Avg Rainfall (mm)');
  renderPieChart('disasterPieChart', c.disaster_dist, 'Disaster Types');
  renderDonutChart('riskDonutChart', c.risk_dist, 'Risk Levels');
  renderBarChart('alertStatusChart', c.alert_dist, 'Alert Status');
  renderBarChart('weatherCondChart', c.weather_cond, 'Weather Conditions');
  renderScatterPlotly('scatterPlot', c.scatter_data);
}
