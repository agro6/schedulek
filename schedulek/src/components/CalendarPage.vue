<template>
<div>Lessons</div>

  <table>
    <thead>
      <tr>
        <th>date</th>
        <th>lesson_number hour</th>
        <th>Subject</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="l in lessons" :key="l.id">
        <td>{{ l.date }}</td>
        <td>
          {{ l.lesson_number }}

          </td>
        <td>{{ l.subject }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'CalendarPage',
  props: {
    studentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      lessons: []
    }
  },
  async created() {
    try {
      const response = await fetch(`http://localhost:5000/lessons/11`);
      const data = await response.json();
      this.lessons = data.lessons;
    } catch (error) {
      console.error(error);
    }
}
}
</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  margin-top: 20px;
}

th,
td {
  text-align: left;
  padding: 8px;
  display: inline-block;
}

th {
  background-color: #4CAF50;
  color: gray;
}

div {
  height: 20px;
  width: 20px;
  display: table-cell;
}

.wage-1 {
  background-color: rgba(76, 175, 80, 0.5);
}

.wage-2 {
  background-color: rgba(45, 158, 73, 0.5);
}

.wage-3 {
  background-color: rgba(13, 139, 59, 0.5);
}

.wage-4 {
  background-color: rgba(8, 104, 45, 0.5);
}

.wage-5 {
  background-color: rgba(5, 75, 32, 0.5);
}
</style>
