import Vue from 'vue'
import Router from 'vue-router'
import Splash from '@/components/Splash'
import Map from '@/components/Map'
import Login from '@/components/Login'
import AccountManager from '@/components/AccountManager'
import CompareBots from '@/components/CompareBots'

import Analytics from '@/components/Analytics'
import SysSummary from '@/components/AnalyticsComponents/SysSummary'
import RobotHealth from '@/components/AnalyticsComponents/RobotHealth'
import CPUTemp from '@/components/AnalyticsComponents/CPUTemp'
import PowerDraw from '@/components/AnalyticsComponents/PowerDraw'
import HistData from '@/components/AnalyticsComponents/HistData'
import HistHealth from '@/components/AnalyticsComponents/HistHealth'

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
      component: Analytics,
      children: [
        {
          path: '',
          component: SysSummary
        },
        {
          path: 'sys-summary',
          component: SysSummary
        },
        {
          path: 'robot-health',
          component: RobotHealth
        },
        {
          path: 'cpu-temp',
          component: CPUTemp
        },
        {
          path: 'power-draw',
          component: PowerDraw
        },
        {
          path: 'hist-data',
          component: HistData
        },
        {
          path: 'hist-health',
          component: HistHealth
        }
      ]
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
