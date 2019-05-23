let myChart = document.getElementById('leaderChart').getContext('2d');
let barChart = new Chart(myChart, {
    type: 'bar',
    data: {
        labels: [UserData, UserData, 'Linus', 'Totte'],
        datasets: [{
            label: 'HomeCoins',
            data: [
                UserData,
                UserData,
                6666,
                4000
            ],
            backgroundColor: ['white', 'black', 'blue', 'green'],
        }]
    },
    options: {}

});