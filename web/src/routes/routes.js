// Dashboard pages
import DashboardLayout from "@/pages/Dashboard/Layout/DashboardLayout.vue";
import Dashboard from "@/pages/Dashboard/Dashboard.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
    name: "Home",
  },
  {
    path: "/",
    component: DashboardLayout,
    children: [
      {
        path: "dashboard",
        name: "Dashboard",
        components: { default: Dashboard },
      }
    ],
  },
];

export default routes;
