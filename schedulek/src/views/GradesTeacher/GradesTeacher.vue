<template>
  <div>
      <div class="options">
        <router-link class="nav-button" :to="{ name: 'AddGrade' }">Add grade</router-link>
        <router-link class="nav-button" :to="{ name: 'CheckGrades' }">Check grades</router-link>
      </div>
        <router-view/>
    </div>
</template>

<script>
import { useUserStore } from '../../stores/UserStore.js';

export default {
  setup() {
    const userStore = useUserStore();

    return {
      userStore
    };
  },

}
</script>

<style>
.options{
  margin-left: 40px;
  display: flex;
}

</style>