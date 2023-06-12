const form = document.querySelector("#signup-form");

const isPasswordChecked = (pw, pw2) => {
  return pw === pw2 ? true : false;
};

const handleSubmit = async (e) => {
  e.preventDefault();
  const body = new FormData(form);
  const pw = body.get("password");
  const pw2 = body.get("password2");
  const infoDiv = document.querySelector("#info");

  if (isPasswordChecked(pw, pw2)) {
    infoDiv.innerText = "";
    body.set("password", sha256(pw));
    const res = await fetch("/signup", {
      method: "POST",
      body,
    });
    alert("회원가입에 성공했습니다.");
    window.location.pathname = "/login.html";
  } else {
    infoDiv.innerText = "비밀번호를 확인해주세요.";
    infoDiv.style.color = "red";
    form.appendChild(infoDiv);
  }
};

form.addEventListener("submit", handleSubmit);
