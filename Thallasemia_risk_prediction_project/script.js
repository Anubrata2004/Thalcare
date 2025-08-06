const form = document.getElementById('riskForm');
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
    const risk = result.risk_level;

    resultDiv.textContent = `Risk Level Predicted: ${risk.toUpperCase()}`;
    resultDiv.className = risk.toLowerCase();
    resultDiv.style.display = 'block';
  } catch (err) {
    resultDiv.textContent = '⚠️ Error: ' + err.message;
    resultDiv.style.display = 'block';
    resultDiv.className = 'high';
  }
});
