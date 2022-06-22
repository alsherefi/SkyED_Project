// For the form fields username, email, password and confirm password.

const pass = document.getElementById("new_password");
const cpass = document.getElementById("con_password");

// For the putting errors under Each field in case there is an error.

const perr = document.getElementById("perr");
const cperr = document.getElementById("cperr");

const form = document.getElementById("form");

//For conditions
regpass = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_\-=+[\]\\/?<>,.{}])[a-zA-Z0-9!@#$%^&*()_\-=+[\]\\/?<>,.{}]{6,}$/;

err="text-red-500";

form.addEventListener("submit" ,(e) =>
{
  flag = 1;
  perr.innerHTML = "";
  cperr.innerHTML = "";

  perr.removeAttribute("class");
  cperr.removeAttribute("class");

  if (!regpass.test(pass.value)) {
    perr.innerHTML = "Password must have at least one digit, one lower case, one upper case and one special symbol. Length must be more than 5.<br><br>";
    perr.setAttribute("class", err);
    flag = 0;
  }
  if (pass.value !== cpass.value) {
    cperr.innerHTML = "Password Doesn't match<br><br>";
    cperr.setAttribute("class", err);
    flag = 0;
  }
  if (flag == 0)
    e.preventDefault();
});