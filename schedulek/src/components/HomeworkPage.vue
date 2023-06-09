<template>
  <div>
    <NavigationBar /> <!-- Import and use the NavigationBar component -->
    <p>Hello</p> <!-- Display the "Hello" text -->
  </div>
</template>

<script>
import NavigationBar from './NavigationBar.vue'; // Import the NavigationBar component

export default {
  name: 'HomeworkPage',
  components: {
    NavigationBar, // Register the NavigationBar component
  },
}
</script>
