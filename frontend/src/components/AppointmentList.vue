<template>
  <div>
    <h3>Appointment List</h3>
    <div>
      <h4>In Session</h4>
      <div v-for="(patient, appt_id, i) in inSessionPatient" :key="i">
        <span>{{patient.first_name + ' ' + patient.last_name}}</span>
        <button class="btn btn-primary" @click="updateStatus(appt_id, 'Complete')">Complete</button>
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
              console.log( cur.appointments[i]);
              if (cur.appointments[i].status == 'In Session') {
                cur.updateInSession(cur.appointments[i].id, cur.appointments[i].patient)
                //cur.inSessionPatient.push(patient);
                //console.log(patient);
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
        this.appointments[idx].status = status;
        var cur = this;
        this.axios.patch('http://127.0.0.1:8000/api/appointment/' + appointment_id + '/', {status:status})
          .then((response) => {
             console.log('done');
          }).catch(function (error) {
              console.log(error);
          });
        this.updateInSession(appointment_id, this.appointments[idx].patient);
      },
      updateInSession(appointment_id, patient_id) {
        this.axios.get(this.patient_url + patient_id)
          .then((response) => {
            console.log(response.data);
            this.inSessionPatient.push({appointment_id:response.data});
          })
          .catch(function (error) {
              console.log(error);
          });
      },
      getAppointmentById(id) {
        this.appointments.findIndex((appt) => {
          return appt.id == id;
        })
      }
    }
  }
</script>
