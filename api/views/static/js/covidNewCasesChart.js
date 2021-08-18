const country = document.getElementById('country').value

fetch('http://localhost:5000/covid_new_cases/json/' + country)
    .then(response => response.json())
    .then(mongoData => printCharts(mongoData))


function printCharts(mongoData) {
    document.body.classList.add('running')
    barChart(mongoData.result, 'chart')
}


function getUnique(value, index, self) {
    return self.indexOf(value) === index
  }


function barChart(mongoData, id) {
    const yearsInMongoData = mongoData.map(eachRecord => eachRecord.year)
    const records = yearsInMongoData.filter(getUnique).map((year, index) => {
        return {
            label: year,
            data: mongoData.filter(eachRecord => eachRecord.year === year)
                           .map(eachRecord => eachRecord.total_new_cases),
            borderWidth: 1,
            borderColor: styles.color.solids[index],
            backgroundColor: styles.color.alphas[index]
        }
    })

    const data = {
        labels: [
            'jan', 'feb', 'mar', 'apr', 'may', 'jun',
            'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
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
