const country = document.getElementById('country').value
const days = document.getElementById('period').value
const url = `http://localhost:5001/covid_summary/json/${country}?days=${days}`;

fetch(url)
    .then(response => response.json())
    .then(mongoData => displayDashboard(mongoData))


function displayDashboard(mongoData) {
    document.body.classList.add('running');
    barChart(getRecords(mongoData.result), 'chart1', getLabels(mongoData.result));
}


function getLabels(mongoData) {
    return mongoData.map(eachRecord => eachRecord.date).reverse()
}


function getRecords(mongoData) {
    return [{
        label: "New Cases",
        data: mongoData.map(eachRecord => eachRecord.new_cases).reverse(),
        borderWidth: 1,
        borderColor: styles.color.solids[0],
        backgroundColor: styles.color.alphas[0]
    },
    {
        label: "New Deaths",
        data: mongoData.map(eachRecord => eachRecord.new_deaths).reverse(),
        borderWidth: 1,
        borderColor: styles.color.solids[1],
        backgroundColor: styles.color.alphas[2]
    }]
}


function barChart(records, id, xLabels) {
    const data = {
        labels: xLabels,
        datasets: records
    }
    console.log(data);
    const options = {
        legend: {
            position: 'right',
            labels: {
                fontColor: 'grey'
            }
        }
    }
    new Chart(id, {type: 'bar', data, options})
}
