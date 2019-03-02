<template>
  <div>
    <h3>Appointment List</h3>
    <div>
      <h4>In Session</h4>
      <div v-for="(item, i) in inSessionPatient" :key="i">
        <span>{{item.patient.first_name + ' ' + item.patient.last_name}}</span>
        <button class="btn btn-primary" @click="updateStatus(item.id, 'Complete')">Complete</button>
      </div>
    </div>
    <table>
      <tr>
        <th>Status</th>
        <th>ID</th>
        <th>Duration</th>
        <th>Waiting</th>
        <th>Action</th>
      </tr>
      <tr v-if="!appointments || appointments.length == 0">
        <td colspan="100%">Cannot find any appointment</td>
      </tr>
      <tr v-else v-for="(appointment, idx) in appointments" :key="idx">
        <td>{{appointment.status}}</td>
        <td>{{appointment.id}}</td>
        <td>{{appointment.duration}}</td>
        <td>{{waitingTime(appointment.status, appointment.checkin_time)}}</td>
        <td>
          <button v-if="appointment.status == 'Checked In'" class="btn btn-primary btn-sm" @click="updateStatus(appointment.id, 'In Session')">See Now</button>
        </td>
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
      },
      patient_url: {
        type: String
      }
    },
    data()
    {
      return {
        appointments: [],
        canCheckIn:[null,'', 'Rescheduled', 'Confirmed'],
        inSessionPatient:[],
      }
    },
    mounted()
    {
      this.getAppointmentList(true);
    },
    methods: {
      getAppointmentList(init = false)
      {
        var cur = this;
        this.axios.get(this.url).then((response) => {
          cur.appointments = response.data;
          if (init) {
            for (var i in cur.appointments) {
              if (cur.appointments[i].status == 'In Session') {
                cur.updateInSession(cur.appointments[i].id, cur.appointments[i].patient)
              }
            }
          }
        })
      },
      waitingTime(status, checkin_time) {
        if(status != 'Checked In' || checkin_time == null)
          return '';
        var now = Date.now();
        var checkin = Date.parse(checkin_time);
        var diff = now - checkin;
        var hh = Math.floor(diff / 1000 / 60 / 60);
        diff -= hh * 1000 * 60 * 60;
        var mm = Math.floor(diff / 1000 / 60);
        diff -= mm * 1000 * 60;
        return (hh==0? '': hh + 'hr ') + mm +'min';
      },
      updateStatus(appointment_id, status) {
        var idx = this.getAppointmentById(appointment_id);
        this.appointments[idx].status = status;
        this.axios.patch('http://127.0.0.1:8000/api/appointment/' + appointment_id + '/', {status:status})
          .then((response) => {
             console.log('done');
          }).catch(function (error) {
              console.log(error);
          });
        if (status == 'In Session') {
          this.updateInSession(appointment_id, this.appointments[idx].patient);
        } else if (status == 'Complete') {
          var i = this.inSessionPatient.findIndex((appt) => {
            return appt.id == appointment_id;
          });
          this.inSessionPatient.splice(i, 1);
        }
      },
      updateInSession(appointment_id, patient_id) {
        this.axios.get(this.patient_url + patient_id)
          .then((response) => {
            this.inSessionPatient.push({
              id:appointment_id,
              patient:response.data
            });
          })
          .catch(function (error) {
              console.log(error);
          });
      },
      getAppointmentById(id) {
        var idx = this.appointments.findIndex((appt) => {
          return appt.id == id;
        })
        return idx;
      }
    }
  }
</script>
