document.addEventListener("DOMContentLoaded", function () {
    const formerCards = document.querySelectorAll(".former-card");

    formerCards.forEach((card) => {
        const defaultImage = card.querySelector(".default-image");
        const hoverImage = card.querySelector(".hover-image");

        // For desktop hover
        card.addEventListener("mouseenter", () => {
            defaultImage.style.opacity = 0;
            hoverImage.style.opacity = 1;
        });

        card.addEventListener("mouseleave", () => {
            defaultImage.style.opacity = 1;
            hoverImage.style.opacity = 0;
        });

        // For mobile touch
        card.addEventListener("touchstart", () => {
            if (defaultImage.style.opacity === "0") {
                defaultImage.style.opacity = 1;
                hoverImage.style.opacity = 0;
            } else {
                defaultImage.style.opacity = 0;
                hoverImage.style.opacity = 1;
            }
        });
    });
});