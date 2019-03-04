// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import appointmentlist from './components/AppointmentList'
import checkinlist from './components/CheckInList'
import waitingchart from './components/WaitingChart'
//import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'
import '@/assets/css/tailwind.css'
import '@/assets/css/main.css'
import VueSweetalert2 from 'vue-sweetalert2';

Vue.config.productionTip = false
Vue.use(VueAxios, axios)
Vue.use(VueSweetalert2)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  //router,
  components: {
    App,
    appointmentlist,
    checkinlist,
    waitingchart,
  },
})
