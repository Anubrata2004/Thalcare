const form = document.getElementById('donorForm');
const resultDiv = document.getElementById('result');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  resultDiv.style.display = 'none';
  resultDiv.textContent = '';
  resultDiv.className = '';

  const formData = new FormData(form);
  const data = {};
  formData.forEach((v, k) => {
    data[k] = isNaN(v) ? v : Number(v);
  });

  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Server error');
    }

    const result = await response.json();

    if (result.available === 1) {
      resultDiv.textContent = '✅ Donor is likely AVAILABLE.';
      resultDiv.className = 'available';
    } else {
      resultDiv.textContent = '❌ Donor is likely NOT AVAILABLE.';
      resultDiv.className = 'not-available';
    }
    resultDiv.style.display = 'block';
  } catch (err) {
    resultDiv.textContent = '⚠️ Error: ' + err.message;
    resultDiv.style.display = 'block';
    resultDiv.className = 'not-available';
  }
});
