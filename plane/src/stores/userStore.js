import { onMounted, ref } from "vue";

import { defineStore } from "pinia";
import axios from "axios";
import Cookies from "js-cookie";

// Установка заголовков CSRF и авторизации
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get("csrftoken");

const useUserStore = defineStore("UserStore", () => {
    const isAuthenticated = ref(false);
    const username = ref("");
    const userId = ref();

    async function fetchUser() {
        try {
            console.log("CSRF Token: ", Cookies.get("csrftoken"));

            const response = await axios.post("/api/user/info/", null, {
                headers: {
                    "X-CSRFToken": Cookies.get("csrftoken"),
                }
            });
            isAuthenticated.value = response.data.is_authenticated;
            username.value = response.data.username;
            userId.value = response.data.user_id;
        } catch (error) {
            console.error("Error fetching user:", error);
            if (error.response) {
                console.error("Response error:", error.response.data);
            }
        }
    }
    

    onMounted(() => {
        fetchUser();
    });

    return {
        isAuthenticated,
        username,
        userId,
        fetchUser,
    };
});

export default useUserStore;
