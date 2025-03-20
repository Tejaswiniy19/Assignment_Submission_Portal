const loginForm = document.querySelector('.login-form');
const signupForm = document.querySelector('.signup-form');

function swapPos(btn) {
    const isSignupSwitch = btn.classList.contains('signup-switch');
    signupForm.classList.toggle('above', isSignupSwitch);
    loginForm.classList.toggle('above', !isSignupSwitch);
    signupForm.classList.toggle('below', !isSignupSwitch);
    loginForm.classList.toggle('below', isSignupSwitch);
}