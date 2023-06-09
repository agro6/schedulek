<template>
  <div>
    <div class="options">
      <router-link class="nav-button" :to="{ name: 'CheckAttendanceTeacher' }">Check attendance</router-link>
      <router-link class="nav-button" :to="{ name: 'EditAttendanceTeacher' }">Edit attendance</router-link>
    </div>
      <router-view/>
  </div>
</template>

<script>
export default {

}
</script>

<style>
.options{
  margin-left: 40px;
  display: flex;
}
</style>