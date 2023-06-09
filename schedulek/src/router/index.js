import { createRouter, createWebHistory } from 'vue-router'
import CalendarPage from '../views/CalendarPage/CalendarPage.vue'
import TimetablePage from '../views/TimetablePage/TimetablePage.vue'
import GradesPage from '../views/GradesPage/GradesPage.vue'
import HomeworkPage from '../views/HomeworkPage/HomeworkPage.vue'
import MessagesPage from '../views/MessagesPage/MessagesPage.vue'
import LoginPage from '../views/LoginPage.vue'
import LogoutPage from '../views/LogoutPage.vue'
import TimetableTeacher from '../views/TimetableTeacher/TimetableTeacher.vue'
import AttendanceTeacher from '../views/AttendanceTeacher/AttendanceTeacher.vue'
import GradesTeacher from '../views/GradesTeacher/GradesTeacher.vue'
import HomeworkTeacher from '../views/HomeworkTeacher/HomeworkTeacher.vue'
import MessagesTeacher from '../views/MessagesTeacher/MessagesTeacher.vue'
import CheckAttendanceTeacher from '../views/AttendanceTeacher/CheckAttendanceTeacher.vue'
import EditAttendanceTeacher from '../views/AttendanceTeacher/EditAttendanceTeacher.vue'
import AddGrade from '../views/GradesTeacher/AddGrade.vue'
import CheckGrades from '../views/GradesTeacher/CheckGrades.vue'
import AddHomework from '../views/HomeworkTeacher/AddHomework.vue'
import ManageHomework from '../views/HomeworkTeacher/ManageHomework.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'

  },
  {
    path: '/calendar',
    name: 'CalendarPage',
    component: CalendarPage

  },
  {
    path: '/timetable',
    name: 'TimetablePage',
    component: TimetablePage

  },
  {
    path: '/grades',
    name: 'GradesPage',
    component: GradesPage

  },
  {
    path: '/homework',
    name: 'HomeworkPage',
    component: HomeworkPage

  },
  {
    path: '/messages',
    name: 'MessagesPage',
    component: MessagesPage

  },
  
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  },
  {
    path: '/loggedout',
    name: 'LogoutPage',
    component: LogoutPage
  },
  {
    path: '/timetable/teacher',
    name: 'TimetableTeacher',
    component: TimetableTeacher
  },
  {
    path: '/attendance/teacher',
    name: 'AttendanceTeacher',
    component: AttendanceTeacher,
    children: [
      {
        path: 'check',
        name: 'CheckAttendanceTeacher',
        component: CheckAttendanceTeacher
      },
      {
        path: 'edit',
        name: 'EditAttendanceTeacher',
        component: EditAttendanceTeacher
      }
    ]
  },
  {
    path: '/grades/teacher',
    name: 'GradesTeacher',
    component: GradesTeacher,
    children: [
      {
        path: 'check',
        name: 'CheckGrades',
        component: CheckGrades
      },
      {
        path: 'add',
        name: 'AddGrade',
        component: AddGrade
      }
    ]
  },
  {
    path: '/homework/teacher',
    name: 'HomeworkTeacher',
    component: HomeworkTeacher,
    children: [
      {
        path: 'add',
        name: 'AddHomework',
        component: AddHomework
      },
      {
        path: 'manage',
        name: 'ManageHomework',
        component: ManageHomework
      }
    ]
  },
  {
    path: '/messages/teacher',
    name: 'MessagesTeacher',
    component: MessagesTeacher
  },

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.replace({ path: '*', redirect: '/' })
export default router