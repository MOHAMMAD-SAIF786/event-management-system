const menuToggle = document.getElementById("menuToggle");
const navMenu = document.getElementById("navMenu");

if (menuToggle && navMenu) {

    menuToggle.addEventListener("click", () => {
        navMenu.classList.toggle("active");

        menuToggle.innerHTML = navMenu.classList.contains("active")
            ? '<i class="fa-solid fa-xmark"></i>'
            : '<i class="fa-solid fa-bars"></i>';
    });

    const dropdowns = document.querySelectorAll(".dropdown");

    dropdowns.forEach(drop => {

        const link = drop.querySelector("a");

        link.addEventListener("click", function (e) {

            if (window.innerWidth <= 991) {

                e.preventDefault();
                drop.classList.toggle("active");

            }

        });

    });

    document.querySelectorAll(".nav-menu a").forEach(link => {

        link.addEventListener("click", () => {

            if (window.innerWidth <= 991) {

                navMenu.classList.remove("active");

                menuToggle.innerHTML =
                    '<i class="fa-solid fa-bars"></i>';

            }

        });

    });

}

const header = document.getElementById("header");

window.addEventListener("scroll", () => {

    if (window.scrollY > 50) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }

});