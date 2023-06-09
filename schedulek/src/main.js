import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCXh48qMJir9s1S8xvycOHBPrGd_fbwR8A",
  authDomain: "schedulek-fcc88.firebaseapp.com",
  projectId: "schedulek-fcc88",
  storageBucket: "schedulek-fcc88.appspot.com",
  messagingSenderId: "13103807891",
  appId: "1:13103807891:web:695ec5b274538e65ecbc66"
};

// Initialize Firebase
initializeApp(firebaseConfig);

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons'
library.add(faRightFromBracket)

import { faCalendarDays } from '@fortawesome/free-regular-svg-icons'
library.add(faCalendarDays)

import { faClock } from '@fortawesome/free-solid-svg-icons'
library.add(faClock)

createApp(App).component('font-awesome-icon', FontAwesomeIcon).use(router).use(createPinia()).mount('#app')
