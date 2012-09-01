google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(loadData);

function loadData() {
    myData = { id: $('#id_mutualFundTitle').attr('data-id') };
    $.ajax({ url: '/fondo-mutuo/chart-data'
        , data: myData
        , dataType: 'json'
        , success: drawChart
        , error: drawChart});
}

function drawChart(pDataTable, var1, var2) {
    for ( lIndex in pDataTable.rows ) {
        pDataTable.rows[lIndex]['c'][0]['v'] = new Date(pDataTable.rows[lIndex]['c'][0]['v']);
    }
    var data = new google.visualization.DataTable(pDataTable);
    var chart = new google.visualization.LineChart(document.getElementById('id_chart'));
    chart.draw(data, {width: 515, height: 240});
}
