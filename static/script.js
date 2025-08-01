let currentInput = '';

function appendToDisplay(value) {
    currentInput += value;
    document.getElementById('display').value = currentInput;
}

function clearDisplay() {
    currentInput = '';
    document.getElementById('display').value = '';
    document.getElementById('result').textContent = '';
}

function backspace() {
    currentInput = currentInput.slice(0, -1);
    document.getElementById('display').value = currentInput;
}

async function calculate() {
    const expression = currentInput;
    if (!expression) return;

    try {
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expression })
        });

        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('result').textContent = `Result: ${data.result}`;
            currentInput = data.result.toString();
            document.getElementById('display').value = currentInput;
        } else {
            document.getElementById('result').textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        document.getElementById('result').textContent = `Error: ${error.message}`;
    }
}

// Keyboard support
document.addEventListener('keydown', (event) => {
    const key = event.key;
    
    if (/[0-9+\-*/.()]/.test(key)) {
        appendToDisplay(key);
    } else if (key === 'Enter') {
        calculate();
    } else if (key === 'Backspace') {
        backspace();
    } else if (key === 'Escape') {
        clearDisplay();
    } else if (key === '.') {
        appendToDisplay('.');
    }
});