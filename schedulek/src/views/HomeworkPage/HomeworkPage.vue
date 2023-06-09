<template>
  <div>
    Homework
  </div>
<div class="container">
<div v-for="l in homework" :key="l.id" class="card">
  <div class="header">
      <div class="content">
         <span class="title">{{l.subject}} {{l.deadline_date}}</span>
         <p class="message">{{l.teacher}} {{l.summary}}</p>
         </div>
         <div class="actions">
            <button type="button" class="answer">Answer now</button>
            </div>
            </div>
            </div>
            </div>


</template>

<script>
export default {
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
      const response = await fetch(`http://localhost:5000/homework/11`);
      const data = await response.json();
      this.homework = data.homework;
    } catch (error) {
      console.error(error);
    }
}
}
</script>
<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.card {
  overflow: hidden;
  position: relative;
  text-align: left;
  border-radius: 0.5rem;
  max-width: 290px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  background-color: #fff;
}


.dismiss:hover {
  background-color: #ee0d0d;
  border: 2px solid #ee0d0d;
  color: #fff;
}

.header {
  padding: 1.25rem 1rem 1rem 1rem;
}

.image {
  display: flex;
  margin-left: auto;
  margin-right: auto;
  background-color: #e2feee;
  flex-shrink: 0;
  justify-content: center;
  align-items: center;
  width: 3rem;
  height: 3rem;
  border-radius: 9999px;
  animation: animate .6s linear alternate-reverse infinite;
  transition: .6s ease;
}

.image svg {
  color: #0afa2a;
  width: 2rem;
  height: 2rem;
}


.title {
  color: #066e29;
  font-size: 1rem;
  font-weight: 600;
  line-height: 1.5rem;
}

.message {
  margin-top: 0.5rem;
  color: #595b5f;
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.actions {
  margin: 0.75rem 1rem;
}

.answer {
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




</style>