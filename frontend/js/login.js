const form = document.querySelector("#login-form");

let accessToken = null;

const handleSubmit = async (event) => {
  event.preventDefault();
  const body = new FormData(form);
  body.set("password", sha256(body.get("password")));
  const res = await fetch("/login", {
    method: "POST",
    body,
  });
  const data = await res.json();
  accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);

  const infoDiv = document.querySelector("#info");
  infoDiv.innerText = "로그인되었습니다";

  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmit);
