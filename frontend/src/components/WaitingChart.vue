<template>
  <div>
    <div id="curve_chart" class="w-full h-64 mb-4"></div>
    <button class="btn btn-default" type="button" @click="goBack">Go Back</button>
  </div>
</template>
<script>
  export default {
    props:['waitingTimeList'],
    data() {
      return {
        avgWaitingTime: JSON.parse(this.waitingTimeList)
      }
    },
    mounted() {
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(this.drawChart);
    },
    methods: {
      drawChart() {
        var chart = [['Date', 'Waiting Time (min)']];
        for (var date in this.avgWaitingTime) {
          chart.push([date, this.avgWaitingTime[date]]);
        }
        var data = google.visualization.arrayToDataTable(chart);

        var options = {
          title: 'Average Waiting Time',
          curveType: 'function',
          legend: {position: 'bottom'}
        };

        var chart = new google.visualization.AreaChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
      },
      goBack() {
        window.location.href='http://localhost:8000/welcome';
      },
    }
  }
</script>
