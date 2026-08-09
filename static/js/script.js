setTimeout(() => {
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach((flash) => {
    flash.remove();
  });
}, 3000);

const menuButton = document.querySelector(".mobile-nav-button");
const menuMobile = document.querySelector(".navigation-bar");

menuButton.addEventListener("click", () => {
  const menuOpen = menuButton.classList.toggle("active");
  menuMobile.classList.toggle("active");

  if (menuOpen) {
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
  } else {
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
  }
});

const mobileMenuSpans = document.querySelectorAll(".nav-item-bottom");

mobileMenuSpans.forEach(
  (item) => (item.style.animationDelay = `${Math.random() * 0.4}s`),
);

//slider function

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

const emailPattern = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
const pricePattern = /^\d+(\.\d{1,2})?$/;
const timePattern = /^\d{2}:\d{2}:\d{2} (AM|PM)$/;
const fullDatePattern = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (AM|PM)$/;
const datePattern = /^\d{4}-\d{2}-\d{2}$/;

// register form
const errorMessage = document.querySelector(".form_error");
const registerForm = document.querySelector("#register-form");

if (registerForm) {
  registerForm.addEventListener("submit", function (event) {
    const businessName = document
      .getElementById("business-name")
      .value()
      .trim()
      .toLower();
    const businessAddress = document
      .getElementById("business-address")
      .value()
      .trim()
      .toLower();
    const businessTelephone = document
      .getElementById("business-telephone")
      .value()
      .trim();
    const businessEmail = document
      .getElementById("business-email")
      .value()
      .trim()
      .toLower();

    if (!businessName) {
      event.preventDefault();
      errorMessage.textContent = "Please enter a business name!";
      return;
    }

    if (businessName.length < 5) {
      event.preventDefault();

      errorMessage.textContent = "Business name greater than 5 characters!";
      return;
    }

    if (!businessAddress) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a business address!";
      return;
    }

    if (businessAddress.length < 30) {
      event.preventDefault();

      errorMessage.textContent =
        "Business address must be greater than 30 characters!";
      return;
    }

    if (!businessTelephone) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a business telephone number!";
      return;
    }

    if (businessTelephone.length < 10) {
      event.preventDefault();

      errorMessage.textContent =
        "Business telephone number must be greater than 10 characters!";
      return;
    }

    if (!businessEmail) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a business email address!";
      return;
    }

    if (!emailPattern.test(businessEmail)) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a valid business email address!";
      return;
    }

    const title = document.getElementById("title").value().trim().toLower();
    const fname = document.getElementById("fname").value().trim().toLower();
    const sname = document.getElementById("sname").value().trim().toLower();
    const email = document.getElementById("email").value().trim().toLower();
    const role = document.getElementById("role").value().trim().toLower();
    const password = document.getElementById("password").value().trim();
    const confirmPassword = document
      .getElementById("confirm-password")
      .value()
      .trim();

    if (!title) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a title";
      return;
    }

    if (!["dr", "mrs", "miss", "ms", "mr"].includes(title)) {
      event.preventDefault();

      errorMessage.textContent =
        "Please select a title from the list provided!";
      return;
    }

    if (!fname) {
      event.preventDefault();

      errorMessage.textContent = "Please enter your first name!";
      return;
    }

    if (fname.length < 1 || fname.length > 100) {
      event.preventDefault();

      errorMessage.textContent =
        "First name must be greater than 1 and less than 100 characters!";
      return;
    }

    if (sname.length < 1 || sname.length > 100) {
      event.preventDefault();

      errorMessage.textContent =
        "Last name must be greater than 1 and less than 100 characters!";
      return;
    }

    if (!email) {
      event.preventDefault();

      errorMessage.textContent = "Please enter your email address!";
      return;
    }

    if (!emailPattern.test(email)) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a valid email address!";
      return;
    }

    if (email.toLower() == businessEmail.toLower()) {
      event.preventDefault();

      errorMessage.textContent =
        "Please use an email different to the business email!";
      return;
    }

    if (!role) {
      event.preventDefault();

      errorMessage.textContent = "Please select a valid salutation!";
      return;
    }

    if (!["owner", "employee", "manager"].includes(role)) {
      event.preventDefault();

      errorMessage.textContent = "Please select a role from the list provided!";
      return;
    }

    if (!password) {
      event.preventDefault();

      errorMessage.textContent = "Please enter a password!";
      return;
    }

    if (password.length < 10 || password.length > 20) {
      event.preventDefault();

      errorMessage.textContent =
        "Password must be greater than 15 and less than 25 characters!";
      return;
    }

    if (confirmPassword.length < 10 || confirmPassword.length > 20) {
      event.preventDefault();

      errorMessage.textContent =
        "Password must be greater than 15 and less than 25 characters!";
      return;
    }

    if (password == confirmPassword) {
      event.preventDefault();

      errorMessage.textContent = "Passwords must match!";
      return;
    }
  });
}
