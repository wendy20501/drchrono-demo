<template>
  <div>
    <div class="subtitle">Appointment List</div>
    <div class="flex justify-between">
      <span>Date: {{getDate()}}</span>
      <span>Auto update: <ToggleButton @change="switchAutoUpdate" v-model="autoLoad"></ToggleButton></span>
    </div>
    <div>
      <div v-if="loading"><Circle2></Circle2></div>
      <table v-else>
        <tr>
          <th>Status</th>
          <th>Patient</th>
          <th>Schedule</th>
          <th>Waiting</th>
          <th>Action</th>
        </tr>
        <tr v-if="!appointments || displayAppts.length == 0">
          <td colspan="100%">Cannot find any appointment</td>
        </tr>
        <tr v-else v-for="(appointment, idx) in displayAppts" :key="idx">
          <td><span class="badge" :status="appointment.status">{{appointment.status}}</span></td>
          <td>{{appointment.patient_info? appointment.patient_info.first_name + ' ' + appointment.patient_info.last_name : ''}}</td>
          <td>{{getTime(appointment.scheduled_time)}}</td>
          <td><span v-html="waitingTime(appointment.status, appointment.checkin_time)"></span></td>
          <td>
            <button v-if="appointment.status == 'Checked In'" class="btn btn-primary btn-xs" @click="updateStatus(appointment.id, 'In Session')">Meet</button>
            <button v-if="appointment.status == 'In Session'" class="btn btn-info btn-xs" @click="updateStatus(appointment.id, 'Complete')">Complete</button>
            <button class="btn btn-default btn-xs" @click="updatePatient(appointment.patient_info)">Detail</button>
          </td>
        </tr>
      </table>
    </div>
    <div v-if="patient" class="pt-2">
      <div class="subtitle">Appointment Detail</div>
      <div class="item">
        <div></div>
        <div class="text-lg font-bold">{{patient.first_name + ' ' + patient.last_name}}</div>
        <div><span class="font-semibold">Date of birth:</span> {{getDate(patient.date_of_birth)}}</div>
        <div><span class="font-semibold">Gender:</span> {{patient.gender}}</div>
      </div>
    </div>
  </div>
</template>
<script>
  import {Circle2} from 'vue-loading-spinner';
  import { ToggleButton } from 'vue-js-toggle-button';
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
        displayAppts: [],
        appointments: [],
        canCheckIn:[null,'', 'Rescheduled', 'Confirmed'],
        finished: 0,
        loading: true,
        autoLoad:false,
        timeout: null,
        patient: null,
      }
    },
    components : {
      Circle2,
      ToggleButton
    },
    mounted()
    {
      this.axios.interceptors.request.use((config) => {
        config.headers['X-Requested-With'] = 'XMLHttpRequest';
        let regex = /.*csrftoken=([^;.]*).*$/;
        config.headers['X-CSRFToken'] = jQuery("[name=csrfmiddlewaretoken]").val();
        return config
      });
      this.getAppointmentList();

    },
    watch: {
      finished: function(val) {
        if (val == this.appointments.length) {
          this.loading = false;
          this.displayAppts = this.appointments;
        }
      }
    },
    methods: {
      getAppointmentList()
      {
        this.loading = true;
        var cur = this;
        this.axios.get(this.url, {params:{date:this.getDate()}}).then((response) => {
          cur.appointments = response.data;
          this.finished = 0;
          for (var i in cur.appointments) {
            cur.getPatientInfo(i);
          }
        })
      },
      updateStatus(appt_id, status) {
        var idx = this.displayAppts.findIndex((appt) => {
          return appt.id == appt_id;
        });
        console.log("update status:" + idx);
        this.appointments[idx].status = status;
        this.axios.patch('http://localhost:8000/api/appointment/' + appt_id + '/', {status:status})
          .then((response) => {
             console.log('done');
          }).catch(function (error) {
              console.log(error);
          });
      },
      getPatientInfo(idx) {
        var cur = this;
        this.axios.get(this.patient_url + this.appointments[idx].patient + '/')
          .then((response) => {
            cur.appointments[idx].patient_info = response.data;
            cur.finished++;
          })
          .catch(function (error) {
              console.log(error);
          });
      },
      updatePatient(info) {
        this.patient = info;
        console.log(this.patient);
      },
      getTime(timestring) {
        var time = new Date(timestring)
        var hh = time.getHours();
        var mm = time.getMinutes();
        return (hh > 9 ? hh: '0' + hh) + ":" + (mm > 9 ? mm: '0' + mm);
      },
      getDate(daystring = null) {
        var day = daystring ? new Date(daystring) : new Date();
        var dd = day.getDate();
        var mm = day.getMonth() + 1;
        var yyyy = day.getFullYear();
        return yyyy + '-' + mm + '-' + dd;
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
        var result = hh > 0? '<span class="text-red">':'<span>';

        return result + (hh==0? '': hh + 'hr ') + mm +'min</span>';
      },
      autoUpdate() {
          if (this.autoLoad) {
            this.getAppointmentList();
            setTimeout(this.autoUpdate, 5000);
          }
      },
      switchAutoUpdate() {
        if(this.autoLoad) {
          this.autoUpdate();
        } else {
          clearTimeout(this.timeout);
        }
      }
    }
  }
</script>
