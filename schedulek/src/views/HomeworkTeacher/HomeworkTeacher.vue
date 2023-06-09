<template>
  <div>
      <div class="options">
        <router-link class="nav-button" :to="{ name: 'AddHomework' }">Add homework</router-link>
        <router-link class="nav-button" :to="{ name: 'ManageHomework' }">Manage homework</router-link>
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