<template>
  <table>
    <thead>
      <tr>
        <th>Subject</th>
        <th>Grades</th>
        <th>Average</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="ga in grades_avg" :key="ga.id">
        <td>{{ ga.subject }}</td>
        <td>
          <div v-for="grade in filteredGrades(ga.subject)" :key="grade.id" :class="getGradeClass(grade.wage)">
            {{ grade.grade }}
          </div>
          </td>
        <td>{{ ga.avg }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'GradesTable',
  props: {
    studentId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      grades: [],
      grades_avg: []
    }
  },
  async created() {
    try {
      const response = await fetch(`http://localhost:5000/grades/11`);
      const data = await response.json();
      this.grades = data.grades;
    } catch (error) {
      console.error(error);
    }
    try {
      const response2 = await fetch(`http://localhost:5000/grades_avg/11`);
      const data2 = await response2.json();
      this.grades_avg = data2.grades_avg;
    } catch (error) {
      console.error(error);
    }
  },
  computed: {
      filteredGrades() {
        return (subject) => {
          return this.grades.filter(grade => grade.subject === subject);
        };
      }
    },
  methods: {
    getGradeClass(wage) {
      return `wage-${wage}`;
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
