<template class="border">
  <div>
    <h3>Appointment List</h3>
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
        <td><button @click="checkIn">Check In</button></td>
      </tr>
    </table>
  </div>
</template>
<script>
  export default {
    props:
    {
      url: {
        type: String
      }
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

        this.axios.get(this.url).then((response) => {
          cur.appointments = response.data;
        })
      },
    }
  }
</script>
