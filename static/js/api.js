const api = axios.create({
    baseURL: "/api",
});

api.interceptors.request.use((config) => {
        const access = localStorage.getItem("access_token");

        if (access) {
            config.headers.Authorization = `Bearer ${access}`;
        }

        return config;

    }, (error) => Promise.reject(error)
);

api.interceptors.response.use((response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (!error.response) {
            return Promise.reject(error);
        }

        if (error.response.status === 401 && !originalRequest._retry) {
            const refresh = localStorage.getItem("refresh_token");

            if (!refresh) {
                localStorage.removeItem("access_token");
                window.location.href = "/login/";
                return Promise.reject(error);
            }

            originalRequest._retry = true;

            try {
                const res = await axios.post("/api/token/refresh/", { refresh });

                const newAccess = res.data.access;
                localStorage.setItem("access_token", newAccess);

                originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                return api(originalRequest);

            }
            catch (refreshErr) {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");

                window.location.href = "/login/";

                return Promise.reject(refreshErr);
            }
        }

        return Promise.reject(error);
    }
);

export default api;
