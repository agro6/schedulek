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
          <td class="grades-column">
            <div v-for="grade in filteredGrades(ga.subject)" :key="grade.id" :class="getGradeClass(grade.wage)">
              {{ grade.grade }}
            </div>
            </td>
          <td>{{ Math.round(ga.avg*100) / 100 }}</td>
        </tr>
      </tbody>
    </table>
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
      const response = await fetch(`http://localhost:5000/grades/${this.userStore.loggedUserId}`);
      const data = await response.json();
      this.grades = data.grades;
    } catch (error) {
      console.error(error);
    }
    try {
      const response2 = await fetch(`http://localhost:5000/grades_avg/${this.userStore.loggedUserId}`);
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
  
  table-layout: fixed;
  margin-top: 20px;
  margin-left: 40px;
  border-spacing: 1px 5px;
}

th,
td {
  text-align: left;
  padding: 8px;
  background-color: #F7F8FED9;
  width: 100px;
}
.grades-column{
  width: 420px;
}
tr{
  margin-bottom: 10px;
}

th {
  background-color: #52AB98;
  color: white;
}

div {
  height: 20px;
  width: 20px;
  display: table-cell;
  text-align: center;
  color: white;
}

.wage-1 {
  background-color: rgba(216, 16, 16, 0.74);
}

.wage-2 {
  background-color: rgba(197, 93, 93, 0.74);
}

.wage-3 {
  background-color: rgba(179, 131, 29, 0.5));
}

.wage-4 {
  background-color: rgba(46, 163, 36, 0.5);
}

.wage-5 {
  background-color: rgba(9, 138, 20, 0.884);
}
</style>
