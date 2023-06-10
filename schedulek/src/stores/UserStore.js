import { defineStore } from 'pinia'

export const useUserStore = defineStore('userStore', {
  state: () => ({
    email: '',
    type: '',
    name: '',
    last_name:'',
    loggedUserId:''
  }),
  actions: {
    storeEmail(email) {
      this.email = email
    },
    storeType(type) {
      this.type = type
    },
    storeName(name) {
      this.name = name
    },
    storeLastName(lastname) {
      this.last_name = lastname
    },
    storeLoggedUserId(loggedUserId) {
      this.loggedUserId = loggedUserId;
    },
  }

})