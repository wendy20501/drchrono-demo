<template>
  <div>
    <h3>Appoint List</h3>
    <table>
      <tr>
        <th>Status</th>
        <th>ID</th>
        <th>Duration</th>
        <th>Action</th>
      </tr>
      <tr v-for="(appointment, idx) in appointments" :key="idx">
        <td>{{appointment.status}}</td>
        <td>{{appointment.id}}</td>
        <td>{{appointment.duration}}</td>
        <td><button v-if="canCheckIn.includes(appointment.status)" @click="checkIn">Check In</button></td>
      </tr>
    </table>
  </div>
</template>
<script>
  export default {
    props:
    {
      url
    },
    data()
    {
      return {
        appointments: [],
        canCheckIn:[null,'', 'Rescheduled', 'Confirmed']
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
        var API_URL = 'http://127.0.0.1:8080';

        this.axios.get(`${API_URL}/api/appointment`).then((response) => {
          cur.appointments = response.data;
        })
      },
    }
  }
</script>
