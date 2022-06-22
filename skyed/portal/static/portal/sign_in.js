// For the form fields username, email, password and confirm password.

const email = document.getElementById("email");
const pass = document.getElementById("password");

// For the putting errors under Each field in case there is an error.

const eerr = document.getElementById("eerr");
const perr = document.getElementById("perr");

const form = document.getElementById("form");

//For conditions
regmail = /^[A-Za-z0-9!#$%^&*'/.,`~|\-_?+=]+@[A-Za-z0-9]+(\.[a-zA-Z]{2,})+$/;


err = "text-red-500";

form.addEventListener("submit" ,(e) =>
{
  flag = 1;
  eerr.innerHTML = "";
  perr.innerHTML = "";

  eerr.removeAttribute("class");
  perr.removeAttribute("class");

  if (!regmail.test(email.value)) {
    eerr.innerHTML = "Please enter a valid email address. For example name@dept.collage.uni.com<br><br>";
    eerr.setAttribute("class", err);
    flag = 0;
  }
  if (pass.value.length <= 0) {
    perr.innerHTML = "Please enter a password<br><br>";
    perr.setAttribute("class", err);
    flag = 0;
  }
  if (flag == 0)
    e.preventDefault();
});
