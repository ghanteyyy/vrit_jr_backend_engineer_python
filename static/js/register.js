const form = document.getElementById("register-form");


form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    const payload = {
        name: formData.get("name"),
        email: formData.get("email"),
        password: formData.get("password"),
        date_of_birth: formData.get("date_of_birth"),
    };

    try {
        const response = await fetch("/api/auth/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if(!data.status){
            error = document.querySelector('.error');
            error.style.display = 'block';

            error.innerHTML = data.message;

            return false;
        }

        else{
            localStorage.setItem("access_token", data.token.access);
            localStorage.setItem("refresh_token", data.token.refresh);

            window.location.href = '/dashboard'
        }

    } catch (err) {
        error = document.querySelector('.error');
        error.style.display = 'block';

        error.innerHTML = err;
    }
});


function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
