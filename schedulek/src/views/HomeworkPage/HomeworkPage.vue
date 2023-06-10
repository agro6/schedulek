<template>
  <div>
    <h2>Homework</h2>
    <div class="homework-container">
      <div v-for="l in homework" :key="l.id" class="homework-card">
        <div class="homework-header">
          <div class="homework-content">
            <span class="homework-title">{{ l.subject }} {{ l.deadline_date }}</span>
            <p class="homework-message">{{ l.teacher }} {{ l.summary }}</p>
          </div>
          <div class="homework-actions">
            <button type="button" class="homework-answer">Answer now</button>
          </div>
        </div>
      </div>
    </div>
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
  name: 'HomeworkPage',
  props: {
    studentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      homework: []
    }
  },
  async created() {
    try {
      const response = await fetch(`http://localhost:5000/homework/${this.userStore.loggedUserId}`);
      const data = await response.json();
      this.homework = data.homework;
    } catch (error) {
      console.error(error);
    }
  }
}
</script>
<style scoped>
h2 {
  color: #066e29;
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.homework-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.homework-card {
  overflow: hidden;
  position: relative;
  text-align: left;
  border-radius: 0.5rem;
  width: 290px;
  height: 180px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  background-color: #fff;
  margin-bottom: 20px;
}

.homework-header {
  padding: 1.25rem 1rem 1rem 1rem;
}

.homework-title {
  color: #066e29;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.5rem;
}

.homework-message {
  margin-top: 0.5rem;
  color: #595b5f;
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.homework-actions {
  margin: 0.75rem 1rem;
}

.homework-answer {
  display: inline-flex;
  padding: 0.5rem 1rem;
  background-color: #1aa06d;
  color: #ffffff;
  font-size: 1rem;
  line-height: 1.5rem;
  font-weight: 500;
  justify-content: center;
  width: 100%;
  border-radius: 0.375rem;
  border: none;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.homework-answer:hover {
  background-color: #128d5d;
}
</style>
