import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import Register from '@/views/Register.vue'
import Search from '@/views/Search.vue'
import Result from '@/views/Result.vue'
import ResultView from '@/views/ResultView.vue'
import Manager from '@/views/Manager.vue'

const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/about', name: 'About', component: About },
    { path: '/Manager', name: 'Manager', component: Manager },
    { path: '/register', name: 'Register', component: Register },
    { path: '/search', name: 'Search', component: Search },
    {
        path: '/result:plate', name: 'Result', component: Result,
        children: [
            { path: '', name: 'ResultView', component: ResultView }
        ]
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router