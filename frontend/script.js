let priceChart = null;
let pieChart = null;
let currentTicker = "";

function formatIndianLargeNumbers(num) {
  if (!num || isNaN(num)) return "N/A";
  const sign = num < 0 ? "-" : "";
  const absNum = Math.abs(num);

  // 1 Lakh Crore = 1,00,00,00,00,000 (10^12)
  if (absNum >= 1e12) {
    return sign + "₹" + (absNum / 1e12).toFixed(2) + " Lakh Cr";
  }
  // 1 Crore = 1,00,00,000 (10^7)
  else if (absNum >= 1e7) {
    const formattedCrore = new Intl.NumberFormat("en-IN", {
      maximumFractionDigits: 2,
    }).format(absNum / 1e7);
    return sign + "₹" + formattedCrore + " Cr";
  }
  // 1 Lakh = 1,00,000 (10^5)
  else if (absNum >= 1e5) {
    const formattedLakh = new Intl.NumberFormat("en-IN", {
      maximumFractionDigits: 2,
    }).format(absNum / 1e5);
    return sign + "₹" + formattedLakh + " Lakh";
  }
  // Below 1 Lakh
  else {
    return (
      sign +
      "₹" +
      new Intl.NumberFormat("en-IN", { maximumFractionDigits: 2 }).format(
        absNum,
      )
    );
  }
}

function renderCharts(ticker, chartData, verdictText) {
  // HISTORICAL LINE CHART
  const ctxLine = document.getElementById("priceChart").getContext("2d");
  if (priceChart) priceChart.destroy();

  const labels = chartData.map((item) => item.date);
  const dataPoints = chartData.map((item) => item.price);

  const isUp = dataPoints[dataPoints.length - 1] >= dataPoints[0];

  const gradient = ctxLine.createLinearGradient(0, 0, 0, 320);
  gradient.addColorStop(
    0,
    isUp ? "rgba(0, 243, 255, 0.35)" : "rgba(157, 78, 221, 0.35)",
  );
  gradient.addColorStop(1, "rgba(0, 0, 0, 0)");

  priceChart = new Chart(ctxLine, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Close Price",
          data: dataPoints,
          borderColor: isUp ? "#00f3ff" : "#c084fc",
          backgroundColor: gradient,
          borderWidth: 3,
          pointRadius: 0,
          pointHoverRadius: 6,
          fill: true,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: "index", intersect: false },
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: "rgba(22, 18, 38, 0.95)",
          titleColor: "#cbd5e1",
          bodyColor: "#ffffff",
          borderColor: "rgba(255,255,255,0.2)",
          borderWidth: 1,
          padding: 14,
          titleFont: { size: 14 },
          bodyFont: { size: 16, weight: "bold" },
          displayColors: false,
          callbacks: {
            label: function (c) {
              return "₹" + c.parsed.y;
            },
          },
        },
      },
      scales: {
        x: {
          display: true,
          grid: { display: false },
          ticks: { color: "#cbd5e1", font: { size: 13 }, maxTicksLimit: 8 },
        },
        y: {
          display: true,
          position: "right",
          grid: { color: "rgba(255,255,255,0.08)", borderDash: [4, 4] },
          ticks: {
            color: "#ffffff",
            font: { size: 13, weight: "500" },
            callback: (v) => "₹" + v,
          },
        },
      },
    },
  });

  // AI PIE CHART
  const ctxPie = document.getElementById("sentimentPieChart").getContext("2d");
  if (pieChart) pieChart.destroy();

  let buy = 33,
    hold = 34,
    sell = 33;
  const vText = verdictText.toUpperCase();
  if (vText.includes("BUY")) {
    buy = 75;
    hold = 20;
    sell = 5;
  } else if (vText.includes("SELL")) {
    buy = 5;
    hold = 20;
    sell = 75;
  } else if (vText.includes("HOLD")) {
    buy = 20;
    hold = 60;
    sell = 20;
  }

  pieChart = new Chart(ctxPie, {
    type: "doughnut",
    data: {
      labels: ["Bullish", "Neutral", "Bearish"],
      datasets: [
        {
          data: [buy, hold, sell],
          backgroundColor: ["#00f3ff", "#475569", "#9d4edd"],
          borderWidth: 2,
          borderColor: "#161226",
          hoverOffset: 6,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: "65%",
      plugins: {
        legend: {
          display: true,
          position: "right",
          labels: {
            color: "#ffffff",
            usePointStyle: true,
            padding: 25,
            font: { size: 14, weight: "500" },
          },
        },
        tooltip: {
          backgroundColor: "rgba(22, 18, 38, 0.95)",
          bodyColor: "#ffffff",
          borderColor: "rgba(255,255,255,0.2)",
          borderWidth: 1,
          padding: 12,
          bodyFont: { size: 15 },
          callbacks: {
            label: function (c) {
              return ` ${c.label}: ${c.raw}%`;
            },
          },
        },
      },
    },
  });
}

// MAIN ANALYSIS EXECUTION
document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const tickerInput = document.getElementById("tickerInput");
  const ticker = tickerInput.value.trim().toUpperCase();
  if (!ticker) return;

  const analyzeBtn = document.getElementById("analyzeBtn");

  // DISABLE BUTTON TO PREVENT SPAM CLICKS
  analyzeBtn.disabled = true;
  analyzeBtn.innerText = "ANALYZING...";

  const loader = document.getElementById("loader");
  const resultsPanel = document.getElementById("resultsPanel");

  loader.classList.remove("hidden");
  resultsPanel.classList.add("hidden");

  try {
    const response = await fetch(`/api/analyze/${ticker}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "API Failure");

    currentTicker = data.stock_data.ticker;
    document.getElementById("chatTickerName").innerText = currentTicker;

    // Exact Price Formatter for the Live Price
    const priceFormatter = new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    });

    // Calculate Percentage Change from chartData
    let change = 0;
    if (data.chart_data && data.chart_data.length >= 2) {
      const todayPrice = data.chart_data[data.chart_data.length - 1].price;
      const yesterdayPrice = data.chart_data[data.chart_data.length - 2].price;
      change = ((todayPrice - yesterdayPrice) / yesterdayPrice) * 100;
    }

    const isPositive = change >= 0;
    const colorClass = isPositive ? "text-green" : "text-red";
    const bgClass = isPositive ? "bg-green-light" : "bg-red-light";
    const sign = isPositive ? "+" : "";

    document.getElementById("companyName").innerText =
      data.stock_data.company_name;

    document.getElementById("price").innerHTML = data.stock_data.price
      ? `${priceFormatter.format(data.stock_data.price)} 
       <span class="badge-pill ${bgClass} ${colorClass}" style="font-size: 0.9rem; margin-left: 10px; vertical-align: middle;">
           ${sign}${change.toFixed(2)}%
       </span>`
      : "N/A";

    document.getElementById("marketCap").innerText = formatIndianLargeNumbers(
      data.stock_data.market_cap,
    );
    document.getElementById("revenue").innerText = formatIndianLargeNumbers(
      data.stock_data.revenue,
    );
    document.getElementById("peRatio").innerText = data.stock_data.pe_ratio
      ? data.stock_data.pe_ratio.toFixed(2)
      : "N/A";

    document.getElementById("decision").innerText = data.decision;
    document.getElementById("bullCase").innerText = data.bull_case;
    document.getElementById("bearCase").innerText = data.bear_case;

    renderCharts(data.stock_data.ticker, data.chart_data, data.decision);

    loader.classList.add("hidden");
    resultsPanel.classList.remove("hidden");
  } catch (error) {
    loader.classList.add("hidden");
    alert(`Analysis Error: ${error.message}`);
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerText = "ANALYSIS";
  }
});

document.getElementById("tickerInput").addEventListener("keypress", (e) => {
  if (e.key === "Enter") document.getElementById("analyzeBtn").click();
});

// CHAT FEATURE LOGIC
const chatBox = document.getElementById("chatBox");
const chatInput = document.getElementById("chatInput");
const sendChatBtn = document.getElementById("sendChatBtn");

function appendMessage(sender, text) {
  const msgDiv = document.createElement("div");
  msgDiv.className = `chat-message ${sender === "user" ? "user-message" : "ai-message"}`;
  const avatar = sender === "user" ? "U" : "Q";
  msgDiv.innerHTML = `<div class="msg-avatar">${avatar}</div><div class="msg-bubble">${text}</div>`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

sendChatBtn.addEventListener("click", async () => {
  const text = chatInput.value.trim();
  if (!text || !currentTicker) return;

  sendChatBtn.disabled = true; 
  sendChatBtn.innerText = "✈︎";

  appendMessage("user", text);
  chatInput.value = "";

  const loadingId = "loading-" + Date.now();
  const loadingDiv = document.createElement("div");
  loadingDiv.className = "chat-message ai-message";
  loadingDiv.id = loadingId;
  loadingDiv.innerHTML = `<div class="msg-avatar">Q</div><div class="msg-bubble" style="color: var(--cyan);">Thinking...</div>`;
  chatBox.appendChild(loadingDiv);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ticker: currentTicker, message: text }),
    });

    const data = await response.json();
    document.getElementById(loadingId).remove();

    if (!response.ok) throw new Error(data.detail);

    appendMessage("ai", data.answer);
  } catch (error) {
    document.getElementById(loadingId).remove();
    appendMessage(
      "ai",
      `[System Error]: Could not fetch response. ${error.message}`,
    );
  } finally {
    sendChatBtn.disabled = false;
    sendChatBtn.innerHTML = "Send";
  }
});

chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendChatBtn.click();
});

// DYNAMIC MARKET INTELLIGENCE PANEL
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/market-news");
    const data = await response.json();

    if (response.ok) {
      // Update Trending Assets
      const trendingList = document.querySelector(
        ".intel-col:nth-child(1) .clean-list",
      );
      trendingList.innerHTML = ""; // Clear static HTML

      data.trending.forEach((stock) => {
        const isPositive = stock.change >= 0;
        const colorClass = isPositive ? "text-green" : "text-red";
        const bgClass = isPositive ? "bg-green-light" : "bg-red-light";
        const sign = isPositive ? "+" : "";

        trendingList.innerHTML += `
                    <li>
                        <span class="ticker">${stock.ticker}</span> 
                        <span class="badge-pill ${bgClass} ${colorClass}">${sign}${stock.change.toFixed(2)}%</span>
                    </li>
                `;
      });

      // Update System Alerts
      const alertsList = document.querySelector(
        ".intel-col:nth-child(3) .clean-list",
      );
      alertsList.innerHTML = "";

      data.alerts.forEach((alert) => {
        const colorClass = alert.type === "Live" ? "text-red" : "text-cyan";
        alertsList.innerHTML += `
                    <li><span class="${colorClass} font-medium">${alert.type}:</span> ${alert.text}</li>
                `;
      });
    }
  } catch (error) {
    console.error("Failed to load market intelligence:", error);
  }
});
