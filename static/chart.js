
let myChart = document.getElementById('leaderChart').getContext('2d');

let userNames = UserData.map(user => {
    return user[1];
});

let userValues = UserData.map(user => {
    return user[3];
});

let barChart = new Chart(myChart, {
    type: 'bar',
    data: {
        labels: userNames,
        datasets: [{
            label: 'HomeCoins',
            data: userValues,
            backgroundColor: ['rgba(255, 99, 132, 0.2)',
                                'rgba(255, 159, 64, 0.2)',
                                'rgba(75, 192, 192, 0.2)',
                                'rgba(54, 162, 235, 0.2)',
                                'rgba(153, 102, 255, 0.2)',
                                'rgba(201, 203, 207, 0.2)'],
            borderColor: ['rgb(255, 99, 132)',
                        'rgb(255, 159, 64)',
                        'rgb(75, 192, 192)',
                        'rgb(54, 162, 235)',
                        'rgb(153, 102, 255)',
                        'rgb(201, 203, 207)'],
            borderWidth: 1,

        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        },
        layout: {
            padding: {
                left: 0,
                right: 0,
                top: 0,
                bottom: 0
            }
        },
        scales: {
            xAxes: [{
                barPercentage: 0.5,
                barThickness: 50,
                maxBarThickness: 50,
                minBarLength: 2,
                gridLines: {
                    offsetGridLines: true
                }
            }]
        }
    }

});