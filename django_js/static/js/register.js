const usernameField = document.querySelector('#usernameField');
const feedBackArea = document.querySelector(".invalid_feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const passwordField = document.querySelector('#passwordField');
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector("submit-btn");

const handleToggleInput = (e) => { 
    console.log('toggle reached')
    if (showPasswordToggle.textContent === "SHOW") {
        showPasswordToggle.textContent = "HIDE";
        passwordField.setAttribute("type", "text");
    } else {
        showPasswordToggle.textContent = "SHOW";
        passwordField.setAttribute("type", "password");
    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

usernameField.addEventListener('keyup', (e) => { 
    const usernameVal = e.target.value;
    usernameSuccessOutput.textContent=`Checking ${usernameVal}`
    usernameSuccessOutput.style.display = "block";

    usernameField.classList.remove('is-invalid');
    feedBackArea.style.display = 'none';

    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({ username: usernameVal }),
            method: "POST",
        }).then(res => res.json()).then(data => {
            usernameSuccessOutput.style.display = "none";
            if (data.username_error) {
                submitBtn.disabled = true;

                usernameField.classList.add('is-invalid');
                feedBackArea.style.display = 'block';
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`
            } else {
                submitBtn.removeAttribute('disabled');
            }
        });
    }
});