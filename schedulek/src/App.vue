<template>
  <div id="app">
    <div class="top-panel">
      <div class="top-left">
        <div>
          <font-awesome-icon :icon="['far', 'calendar-days']" class="calendar"/>
          <font-awesome-icon :icon="['fas', 'clock']" class="clock"/>
        </div>
        <div class="name">
          SCHEDULEK
        </div>
      </div>
      <div class="top-right" v-if="userStore.email">
        <div class="logout-icon">
          <font-awesome-icon :icon="['fas', 'right-from-bracket']" @click = "logout"/>
        </div>
        <LoggedInfo></LoggedInfo>
      </div>
    </div>
    
    <div v-if="userStore.type == 'student'" class="nav-panel" >
      <div class="nav-group">
        <router-link class="nav-button" to="/calendar">Calendar</router-link>
        <router-link class="nav-button" :to="{name: 'TimetablePage'}">Timetable</router-link>
        <router-link class="nav-button" :to="{name: 'GradesPage'}">Grades</router-link>
        <router-link class="nav-button" :to="{name: 'HomeworkPage'}">Homework</router-link>
      </div>
      <router-link class="nav-button" :to="{name: 'MessagesPage'}">Messages</router-link>
    </div>
    <div v-else-if="userStore.type == 'teacher'" class="nav-panel" >
        <div class="nav-group">
          <router-link class="nav-button" :to="{ name: 'TimetableTeacher' }">Timetable</router-link>
          <router-link class="nav-button" :to="{ name: 'GradesTeacher' }">Grades</router-link>
          <router-link class="nav-button" :to="{ name: 'HomeworkTeacher' }">Homework</router-link>
        </div>
        <router-link class="nav-button" :to="{ name: 'MessagesTeacher' }">Messages</router-link>
      </div>
    <router-view/>
  </div>

</template>

<script>
// import GradesTable from './components/GradesTable.vue'
// import NavigationBar from './components/NavigationBar.vue'
// import CalendarPage from './components/CalendarPage.vue'
import LoggedInfo from './components/LoggedInfo.vue'
import { useUserStore } from './stores/UserStore.js'
import { getAuth, signOut } from "firebase/auth"

export default {
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
    }
  },
  name: 'App',
  components: {
    LoggedInfo
    // NavigationBar,
    // GradesTable,
    // CalendarPage
  },
  methods: {
    logout() {
      this.$router.push('/loggedout')
      this.userStore.email = ''
      this.userStore.type = ''
      this.userStore.name = ''
      this.userStore.last_name = ''
      const auth = getAuth()
      signOut(auth)
    }
  }
}
</script>

<style>
body{
  margin: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #C8D8E4;
  height: 100vh;
  width: 100vw;
  margin-left: 0px;
  margin-right: 0px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.nav-panel {
  width: 100vw;
  box-sizing: border-box;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  padding-bottom: 20px;
  padding-left: 40px;
  padding-right: 20px;
 
}
.nav-group{
  display: flex;
}
.nav-button{
  display: flex;
  justify-content: center; 
  background: #2B6777;
  border-radius: 20px;
  width: 210px;
  height: 77px;
  font-style: normal;
  font-weight: 600;
  font-size: 20px;
  color: white;
  text-decoration: none;
  margin-right: 20px;
  align-items: center;
}
.top-panel{
  padding-left: 40px;
  padding-right: 40px;
  background-color: white;
  height: 180px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 50px;
  font-weight: bold;
  z-index: 200000;
  width: 100vw;
  box-sizing: border-box;
}
.top-right{
  display: flex;
}
router-view{
  flex-grow: 1;
}
.router-link-active{
  background: #52AB98;
}
.calendar{
  position: relative;
  font-size: 1.5em;
}
.clock{
  position: relative;
  right: 21px;
  top: 15px;
}
.top-left{
  display: flex;
  flex-direction: row;
}
.name{
  display:flex;
  justify-content:center;
  align-items:center;
  position:relative;
  right: 15px;
}

</style>
