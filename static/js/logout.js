import api from "./api.js";


const logout_btn = document.getElementById('logout-btn');

logout_btn.addEventListener("click", async () => {
    try {
        const response = await api.post("/auth/logout/", {
            refresh: localStorage.getItem("refresh_token")
        });

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

         window.location.href = "/login/"
    }
    catch (err) {
        console.log("Status:", err.response?.status);
        console.log("Data:", err.response?.data);
    }
});
