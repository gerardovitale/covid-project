function printCharts(mongoData) {
    document.body.classList.add('running')
    barChart(getRecords(mongoData.result), 'chart')
}


function getUnique(value, index, self) {
    return self.indexOf(value) === index
}


function barChart(records, id) {
    const data = {
        labels: [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ],
        datasets : records
    }

    const options = {
        legend: {
            position: 'right',
            labels: {
                fontColor: 'grey'
            }
        }
    }

    new Chart(id, { type: 'bar', data, options })
}
