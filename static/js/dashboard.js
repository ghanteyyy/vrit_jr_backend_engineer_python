import api from "./api.js";

const dateInput = document.getElementById("expiry_date");

const today = new Date();
today.setDate(today.getDate() + 1);

const yyyy = today.getFullYear();
const mm = String(today.getMonth() + 1).padStart(2, "0");
const dd = String(today.getDate()).padStart(2, "0");

dateInput.min = `${yyyy}-${mm}-${dd}`;


function createShortUrlItem(detail) {
    const short_url = detail.short_url;
    const short_key = detail.short_key;

    const container = document.createElement("div");
    container.className = "short-urls";

    const url = document.createElement("a");
    url.href = short_url;
    url.target = '_blank';
    url.className = "short-url";
    url.textContent = short_url;

    const viewBtn = document.createElement("p");
    viewBtn.className = "btn view-btn";
    viewBtn.textContent = "View";

    const deleteBtn = document.createElement("p");
    deleteBtn.className = "btn delete-btn";
    deleteBtn.textContent = "Delete";

    viewBtn.addEventListener("click", () => {
        window.location.href = `/d/${short_key}`;
    });

    deleteBtn.addEventListener("click", async () => {
        if (!confirm("Are you sure?")) {
            return;
        }

        await api.delete(`/url/shorten/`, {
            data: {
                short_key: short_key,
            }
        });
        container.remove();
    });

    container.appendChild(url);
    container.appendChild(viewBtn);
    container.appendChild(deleteBtn);

    return container;
}


const form = document.querySelector("#shorten-url");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const payload = {
        url: formData.get("url"),
        expiry_date: formData.get("expiry_date"),
    };

    try {
        const response = await api.post("/url/shorten/", payload);
        const data = response.data;

        if (!data.status) {
            const error = document.querySelector(".error");
            error.style.display = "block";
            error.textContent = data.message;
            return;
        }

        else{
            const shorten_url_container = document.querySelector('.shorten-urls');
            const item = createShortUrlItem(data.details);
            shorten_url_container.appendChild(item);
        }

        form.reset();

    } catch (err) {
        const error = document.querySelector(".error");
        error.style.display = "block";

        const msg =
            err.response?.data?.message ||
            err.response?.data?.detail ||
            "Something went wrong.";
        error.textContent = msg;
    }
});



const res = await api.get('/url/shorten/');
const shorten_url_container = document.querySelector('.shorten-urls');

if (res.status == 200) {
    res.data.details.forEach((detail) => {
        const item = createShortUrlItem(detail);
        shorten_url_container.appendChild(item);
    });
}
