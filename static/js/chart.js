const chartElement = document.getElementById("latencyChart");

const jsonData = document.getElementById("latency-data");

if (chartElement && jsonData) {

    const latencyData = JSON.parse(jsonData.textContent);

    const labels = latencyData.map((_, index) => `Request ${index + 1}`);

    new Chart(chartElement, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {
                    label: "Latency (ms)",
                    data: latencyData,
                    borderColor: "#4f46e5",
                    backgroundColor: "rgba(79,70,229,0.1)",
                    fill: true,
                    tension: 0.4
                }

            ]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {
                    display: true
                }

            },

            scales: {

                y: {

                    beginAtZero: true,

                    title: {
                        display: true,
                        text: "Milliseconds"
                    }

                }

            }

        }

    });

}