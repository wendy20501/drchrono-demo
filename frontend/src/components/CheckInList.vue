<template>
  <div class="my-2 w-full mx-auto">
    <p v-if="errors.length" class="text-red">
      <b>Please correct the following error(s):</b>
      <ul>
        <li v-for="error in errors">{{ error }}</li>
      </ul>
    </p>
    <form @submit.prevent="checkform">
      <div class="form-item">
        <label>First name*</label>
        <input name="first_name" required="required" v-model="form.first_name">
      </div>
      <div class="form-item">
        <label>Last name*</label>
        <input name="last_name" required="required" v-model="form.last_name">
      </div>
      <div class="form-item">
        <label>SSN</label>
        <input name="ssn" v-model="form.ssn">
      </div>
      <button class="btn btn-primary" type="button" @click="checkform">Lookup appointment</button>
      <button class="btn btn-default" type="button" @click="goBack">Go Back</button>
    </form>
    <div v-if="showTable" class="mt-4">
      <span v-if="!appointments || appointments.length == 0">Cannot find any appointment</span>
      <table v-else>
        <tr>
          <th>Status</th>
          <th>ID</th>
          <th>Duration</th>
          <th>Action</th>
        </tr>
        <tr v-for="(appointment, idx) in appointments" :key="idx">
          <td class="badge" :status="appointment.status">{{appointment.status || 'Unknown'}}</td>
          <td>{{appointment.id}}</td>
          <td>{{appointment.duration}}</td>
          <td>
            <button v-if="canCheckIn(appointment.status)" class="btn btn-primary" @click="checkIn(appointment.id)">Check In</button>
            <span v-else>Already checked in</span>
          </td>
        </tr>
      </table>
    </div>
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
        errors: [],
        showTable:false,
        form: {
          first_name: "",
          last_name: "",
          ssn:"",
        },
        ssn:""
      }
    },
    mounted() {
      this.axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/;
        config.headers['X-CSRFToken'] = jQuery("[name=csrfmiddlewaretoken]").val();
        return config
      });
    },
    methods: {
      checkform() {
        this.errors = [];
        if (this.form.first_name && this.form.last_name) {
          this.lookup();
          return;
        }

        if (!this.form.first_name) {
          this.errors.push('First name is required.');
        }
        if (!this.form.last_name) {
          this.errors.push('Last name is required.');
        }
      },
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
        this.axios.get(this.appointment_url, {params:{patient:patient_id, date:this.getToday()}})
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
        this.axios.patch('http://localhost:8000/api/appointment/' + appointment_id + '/', {status:'Checked In'})
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
        window.location.href='http://localhost:8000/welcome';
      },
      getToday() {
        var today = new Date();
        var dd = today.getDate();
        var mm = today.getMonth() + 1;
        var yyyy = today.getFullYear();
        return yyyy + '-' + mm + '-' + dd;
      }
    }
  }
</script>
