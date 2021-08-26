const country = document.getElementById('country').value

fetch('http://localhost:5000/covid_new_deaths/json/' + country)
    .then(response => response.json())
    .then(mongoData => printCharts(mongoData))


function getRecords(mongoData) {
    const yearsInMongoData = mongoData.map(eachRecord => eachRecord.year)
    return yearsInMongoData.filter(getUnique).map((year, index) => {
        return {
            label: year,
            data: mongoData.filter(eachRecord => eachRecord.year === year)
                           .map(eachRecord => eachRecord.total_new_deaths),
            borderWidth: 1,
            borderColor: styles.color.solids[index],
            backgroundColor: styles.color.alphas[index]
        }
    })
}
