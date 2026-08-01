// scroll animation

const cards = document.querySelectorAll(".process-card");


window.addEventListener("scroll", () => {

    cards.forEach(card => {

        let position = card.getBoundingClientRect().top;


        if (position < window.innerHeight - 100) {

            card.style.opacity = "1";

        }

    });


});
