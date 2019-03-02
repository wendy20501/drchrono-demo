<template>
  <div>
    <form @submit.prevent="lookup">
      <div>
        <label>First name</label>
        <input name="first_name" v-model="form.first_name">
      </div>
      <div>
        <label>Last name</label>
        <input name="last_name" v-model="form.last_name">
      </div>
      <div>
        <label>SSN</label>
        <input name="ssn" v-model="form.ssn">
      </div>
      <button class="btn btn-primary" type="button" @click="lookup">Lookup appointment</button>
      <button class="btn btn-default" type="button" @click="goBack">Go Back</button>
    </form>
    <table v-if="showTable">
      <tr>
        <th>Status</th>
        <th>ID</th>
        <th>Duration</th>
        <th>Action</th>
      </tr>
      <tr v-if="!appointments || appointments.length == 0">
        <td colspan="100%">Cannot find any appointment</td>
      </tr>
      <tr v-else v-for="(appointment, idx) in appointments" :key="idx">
        <td>{{appointment.status}}</td>
        <td>{{appointment.id}}</td>
        <td>{{appointment.duration}}</td>
        <td>
          <button @click="checkIn(appointment.id)">Check In</button>
          <button v-if="canCheckIn(appointment.status)" @click="checkIn(appointment.id)">Check In</button>
          <span v-else>Already checked in</span>
        </td>
      </tr>
    </table>
  </div>
</template>
<script>
  export default {
    props: {
      patient_url: {
        type: String
      },
      appointment_url: {
        type: String
      },
      checkin_url: {
        type: String
      },
      appointments: {
        type: Array,
        default: []
      },
    },
    data() {
      return {
        showTable:false,
        form: {
          first_name: "",
          last_name: "",
          ssn:"",
        },
        ssn:""
      }
    },
    methods: {
      lookup() {
        this.showTable = true;
        var cur = this;
        this.axios.get(this.patient_url, {params:cur.form})
          .then((response) => {
            if(response.data.length > 0) {
              cur.findAppointments(response.data[0].id);
            } else {
              cur.appointments = [];
            }
          })
          .catch(function (error) {
              console.log(error);
          });
      },
      findAppointments(patient_id) {
        var cur = this;
        this.axios.get(this.appointment_url, {params:{patient_id:patient_id}})
          .then((response) => {
              cur.appointments = Object.keys(response.data).map(function(key) {
                return response.data[key];
              });
            })
          .catch(function (error) {
              console.log(error);
          });
      },
      checkIn(appointment_id) {
        var cur = this;
        this.axios.patch('http://127.0.0.1:8000/api/appointment/' + appointment_id + '/', {status:'Checked In'})
          .then((response) => {
             //cur.goBack();
          }).catch(function (error) {
              console.log(error);
          });
      },
      canCheckIn(status) {
        var canCheckInStatus = ['', "Arrived", "Confirmed", "Rescheduled"]
        return canCheckInStatus.includes(status);
      },
      goBack() {
        window.location.href='http://127.0.0.1:8000/welcome';
      }
    }
  }
</script>
