import Vue from 'vue'
import Router from 'vue-router'
import Splash from '@/components/Splash'
import Map from '@/components/Map'
import Analytics from '@/components/Analytics'
import Login from '@/components/Login'
import AccountManager from '@/components/AccountManager'
import CompareBots from '@/components/CompareBots'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Splash',
      component: Splash
    },
    {
      path: '/map',
      name: 'Map',
      component: Map
    },
    {
      path: '/analytics',
      name: 'Analytics',
      component: Analytics
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/accountmanager',
      name: 'Account Manager',
      component: AccountManager
    },
    {
      path: '/comparebots',
      name: 'Compare Bots',
      component: CompareBots
    }
  ]
})
