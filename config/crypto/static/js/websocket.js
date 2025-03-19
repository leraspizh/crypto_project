document.addEventListener("DOMContentLoaded", function () {
    const table = document.getElementById('crypto-table');
    const chartCanvas = document.getElementById('crypto-chart');

    if (!table || !chartCanvas) {
        console.error("Таблица или график не найдены.");
        return;
    }

    const socket = new WebSocket('ws://localhost:8000/ws/crypto/');

    let historyData = { "BTC/USDT": [], "ETH/USDT": [] };
    let chart;
    let selectedCurrency = "BTC/USDT";
    const maxDataPoints = 50;
    let startTime = Date.now();

    socket.onopen = function () {
        console.log("WebSocket-соединение установлено.");
    };

    socket.onmessage = function (event) {
        try {
            const data = JSON.parse(event.data);
            console.log("Полученные данные:", data);

            if (data.type === "send_price_update") {
                if (!historyData[data.symbol]) {
                    historyData[data.symbol] = [];
                }

                const lastPrice = historyData[data.symbol].length > 0 ? historyData[data.symbol][historyData[data.symbol].length - 1].price : null;
                if (lastPrice !== null && parseFloat(lastPrice).toFixed(2) === parseFloat(data.price).toFixed(2)) {
                    console.log("Цена не изменилась, обновление не требуется.");
                    return;
                }

                historyData[data.symbol].push({
                    price: parseFloat(data.price),
                    timestamp: new Date(data.timestamp).toLocaleTimeString(),
                    timeMs: Date.now() - startTime
                });

                if (historyData[data.symbol].length > maxDataPoints) {
                    historyData[data.symbol].shift();
                }

                updateTable(data);
                updateChart();
            }
        } catch (e) {
            console.error("Ошибка обработки WebSocket-сообщения:", e);
        }
    };

    socket.onclose = function () {
        console.warn("WebSocket-соединение закрыто.");
    };

    function formatPrice(price) {
        return parseFloat(price).toFixed(4).replace(/(\.0+|(\.\d+?)0+)$/, "$1");
    }

    function updateTable(data) {
        let tableBody = table.querySelector("tbody");
        const lastPrice = historyData[data.symbol].length > 1 ? historyData[data.symbol][historyData[data.symbol].length - 2].price : data.price;
        const priceChange = (parseFloat(data.price) - parseFloat(lastPrice)).toFixed(4);
        const percentageChange = ((parseFloat(priceChange) / parseFloat(lastPrice)) * 100).toFixed(2);

        const formattedPrice = formatPrice(data.price);
        const formattedPriceChange = formatPrice(priceChange);
        const formattedPercentageChange = percentageChange === "NaN" ? "0.00" : (parseFloat(percentageChange) > 0 ? `+${percentageChange}` : percentageChange);

        let row = tableBody.querySelector(`tr[data-symbol="${data.symbol}"]`);
        if (!row) {
            row = document.createElement("tr");
            row.setAttribute("data-symbol", data.symbol);
            tableBody.appendChild(row);
        }

        let rowClass = "";
        if (parseFloat(priceChange) > 0) {
            rowClass = "green";
        } else if (parseFloat(priceChange) < 0) {
            rowClass = "red";
        }

        row.innerHTML = `
            <td class="currency-name" data-symbol="${data.symbol}">${data.symbol}</td>
            <td>${formattedPrice}</td>
            <td class="${rowClass}">${formattedPriceChange} (${formattedPercentageChange}%)</td>
        `;
    }

    function updateChart() {
        if (chart) {
            chart.destroy();
        }

        const labels = historyData[selectedCurrency].map(item => {
            const hours = Math.floor(item.timeMs / 3600000);
            const minutes = Math.floor((item.timeMs % 3600000) / 60000);
            return `${hours}:${minutes < 10 ? '0' + minutes : minutes}`;
        });

        const data = {
            labels: labels,
            datasets: [
                {
                    label: selectedCurrency,
                    data: smoothData(historyData[selectedCurrency].map(item => item.price)),
                    borderColor: selectedCurrency === "BTC/USDT" ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 159, 64, 1)',
                    backgroundColor: selectedCurrency === "BTC/USDT" ? 'rgba(75, 192, 192, 0.2)' : 'rgba(255, 159, 64, 0.2)',
                    fill: true,
                    tension: 0.3,
                }
            ]
        };

        const config = {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                animation: {
                    duration: 800,
                    easing: 'easeOutQuad',
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Время'
                        },
                        ticks: {
                            autoSkip: true,
                            maxRotation: 45,
                            minRotation: 0,
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Цена'
                        },
                        ticks: {
                            callback: function (value) { return formatPrice(value); }
                        }
                    }
                }
            }
        };

        chart = new Chart(chartCanvas, config);
    }

    function smoothData(data) {
        return data.map((value, index, arr) => {
            if (index === 0 || index === arr.length - 1) return value;
            return (arr[index - 1] + value + arr[index + 1]) / 3;
        });
    }

    document.body.addEventListener("mouseover", function (event) {
        if (event.target.classList.contains("currency-name")) {
            event.target.style.backgroundColor = "lightgreen";
        }
    });

    document.body.addEventListener("mouseout", function (event) {
        if (event.target.classList.contains("currency-name")) {
            event.target.style.backgroundColor = "";
        }
    });

    document.body.addEventListener("click", function (event) {
        if (event.target.classList.contains("currency-name")) {
            selectedCurrency = event.target.getAttribute("data-symbol");
            updateChart();
        }
    });
});
