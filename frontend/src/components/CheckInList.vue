<template>
  <div>
    <form @submit.prevent="lookup">
      <div>
        <label>First name</label>
        <input name="first_name">
      </div>
      <div>
        <label>Last name</label>
        <input name="last_name">
      </div>
      <div>
        <label>SSN</label>
        <input name="ssn">
      </div>
      <button type="button" @click="lookup">Lookup appointment</button>
    </form>
    <table v-if="showTable">
      <tr>
        <th>Status</th>
        <th>ID</th>
        <th>Duration</th>
        <th>Action</th>
      </tr>
      <tr v-if="appointments || appointments.length == 0">
        <td colspan="100%">Cannot find any appointment</td>
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
    props: {
      url: {
        type: String
      },
      appointments: {
        type: Array,
        default: []
      }
    },
    data() {
      return {
        showTable:false,
        first_name:"",
        last_name:"",
        ssn:""
      }
    },
    methods: {
      lookup() {
        this.showTable = true;
        var cur = this;
        this.axios.get(this.url).then((response) => {
          cur.appointments = response.data;
        })
      }
    }
  }
</script>
