const menuButton = document.querySelector(".mobile-nav-button");
const menuMobile = document.querySelector(".navigation-bar");
menuButton.addEventListener("click", () => {
  const menuOpen = menuButton.classList.toggle("active");
  menuMobile.classList.toggle("active");
  if (menuOpen) {
    document.body.style.overflowY = "hidden";
  } else {
    document.body.style.overflowY = "";
  }
});

const mobileMenuSpans = document.querySelectorAll(".nav-item-bottom");

mobileMenuSpans.forEach(
  (item) => (item.style.animationDelay = `${Math.random() * 0.4}s`),
);
