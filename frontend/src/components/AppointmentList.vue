<template>
  <div>
    <h3>Appoint List</h3>
    <ul>
      <li v-for="appointment in appointments">
          <div>{{appointment.status}}</div>
          <div>{{appointment.doctor}}</div>
      </li>
    </ul>
  </div>
</template>
<script>
  export default {
    data()
    {
      return {
        appointments: []
      }
    }
    ,
    mounted()
    {
      this.getAppointmentList()
    }
    ,
    methods: {
      getAppointmentList()
      {
        var cur = this;
        var API_URL = 'http://localhost:8000';

        this.axios.get(`${API_URL}/api/appointment`).then((response) => {
          cur.appointments = response.data;
        })
      }
    }
  }
</script>
