document.addEventListener("DOMContentLoaded", function () {

    const ctx = document.getElementById("revenueChart");

    if (ctx) {

        new Chart(ctx, {

            type: "line",

            data: {

                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],

                datasets: [{

                    label: "Revenue",

                    data: [25000, 40000, 35000, 50000, 65000, 70000, 85000],

                    borderColor: "#2563eb",

                    backgroundColor: "rgba(37,99,235,.15)",

                    fill: true,

                    tension: .4,

                    pointRadius: 5,

                    pointBackgroundColor: "#2563eb"

                }]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {

                        display: false

                    }

                },

                scales: {

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

    }

});