document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const submitButton = document.querySelector('button[type="submit"]');
  const loadingSpinner = document.getElementById('loading_spinner');

  form.addEventListener('submit', function (event) {
    submitButton.disabled = true;
    submitButton.style.display = 'none';
    loadingSpinner.classList.remove('hidden');
  });
});
