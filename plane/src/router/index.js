import { createRouter, createWebHistory } from 'vue-router';
import ClientsView from '../views/ClientsView.vue';
import TicketsView from '../views/TicketsView.vue';
import BaggagesView from '../views/BaggagesView.vue';
import FlightsView from '../views/FlightsView.vue';
import PlanesView from '../views/PlanesView.vue';
import LoginVue from '@/views/LoginVue.vue';
import MainVue from '@/views/MainVue.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/clients",
      name: "ClientsView",
      component: ClientsView
    },
    {
      path: "/tickets",
      name: "TicketsView",
      component: TicketsView
    },
    {
      path: "/baggages",
      name: "BagaggesView",
      component: BaggagesView
    },
    {
      path: "/flights",
      name: "FlightsView",
      component: FlightsView
    },
    {
      path: "/airplanes",
      name: "PlanesView",
      component: PlanesView
    },
    {
      path: "/login",
      name: "Login",
      component: LoginVue
    },
    {
      path: "/",
      name: "Main",
      component: MainVue
    },
  ]
})

export default router
