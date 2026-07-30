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

const observer = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.2,
  },
);

const elements = document.querySelectorAll(
  ".hidden-right, .hidden-left, .hidden-up",
);

elements.forEach((element) => observer.observe(element));

const featureCards = document.querySelectorAll(".feature");

featureCards.forEach((card, index) => {
  card.style.transitionDelay = `${index * 250}ms`;
});
