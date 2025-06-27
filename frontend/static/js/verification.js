document.addEventListener('DOMContentLoaded', function () {
  const inputs = document.querySelectorAll('.otp-input');
  const otpToken = document.getElementById('otp_token');
  const form = document.getElementById('otp_form');
  const submitBtn = document.getElementById('submit_btn');
  const loadingSpinner = document.getElementById('loading_spinner');
  const resendButton = document.getElementById('resend_button');
  const logoutButton = document.getElementById('logout_btn');

  inputs.forEach((input, index) => {
    input.addEventListener('input', (e) => {
      if (e.target.value.length === 1) {
        if (index < inputs.length - 1) {
          inputs[index + 1].focus();
        }
      }
      updateOtpToken();
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && !e.target.value) {
        if (index > 0) {
          inputs[index - 1].focus();
        }
      }
      updateOtpToken();
    });

    input.addEventListener('paste', (e) => {
      e.preventDefault();
      const pasteData = e.clipboardData.getData('text').trim();
      if (/^\d+$/.test(pasteData) && pasteData.length === inputs.length) {
        pasteData.split('').forEach((char, i) => {
          if (inputs[i]) {
            inputs[i].value = char;
          }
        });
        updateOtpToken();
      }
    });

    input.addEventListener('focus', () => {
      input.classList.add('focused');
    });

    input.addEventListener('blur', () => {
      input.classList.remove('focused');
    });
  });

  function updateOtpToken () {
    otpToken.value = Array.from(inputs)
      .map((input) => input.value)
      .join('');
    if (otpToken.value.length === inputs.length) {
      autoSubmit();
      resendButton.disabled = true;
      resendButton.classList.add('opacity-50', 'cursor-not-allowed');

      logoutButton.disabled = true;
      logoutButton.classList.add('opacity-50', 'cursor-not-allowed');
    }
  }

  function autoSubmit () {
    submitBtn.classList.add('hidden');
    loadingSpinner.classList.remove('hidden');
    form.submit();
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const resendButton = document.getElementById('resend_button');
  const loadingSpinner = document.getElementById('loading_spinners');
  const otpInputs = document.querySelectorAll('.otp-input');
  const submitButton = document.getElementById('submit_btn');
  const logoutButton = document.getElementById('logout_btn');

  if (resendButton) {
    resendButton.addEventListener('click', function (event) {
      event.preventDefault();

      // Disable input fields and buttons
      otpInputs.forEach((input) => {
        input.disabled = true;
        input.classList.add('bg-gray-200', 'cursor-not-allowed');
      });

      submitButton.disabled = true;
      submitButton.classList.add('opacity-50', 'cursor-not-allowed');

      logoutButton.disabled = true;
      logoutButton.classList.add('opacity-50', 'cursor-not-allowed');

      resendButton.style.display = 'none';
      loadingSpinner.classList.remove('hidden');

      fetch(resendButton.href, {
        method: 'GET',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            alert('A new OTP has been sent to your email!');

            // Re-enable inputs and buttons after OTP is sent
            otpInputs.forEach((input) => {
              input.disabled = false;
              input.classList.remove('bg-gray-200', 'cursor-not-allowed');
            });

            submitButton.disabled = false;
            submitButton.classList.remove('opacity-50', 'cursor-not-allowed');

            logoutButton.disabled = false;
            logoutButton.classList.remove('opacity-50', 'cursor-not-allowed');
          } else {
            alert('Failed to resend OTP. Please try again.');
          }

          // Restore Resend button & hide spinner
          resendButton.style.display = 'inline-flex';
          loadingSpinner.classList.add('hidden');
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('An error occurred. Please try again.');

          // Restore Resend button & hide spinner
          resendButton.style.display = 'inline-flex';
          loadingSpinner.classList.add('hidden');
        });
    });
  }
});
