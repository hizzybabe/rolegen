async function generatePrompt() {
    const role = document.getElementById('role').value;
    const responsibilities = document.getElementById('responsibilities').value;
    const tone = document.getElementById('tone').value;
    const additionalInfo = document.getElementById('additional-info').value;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                role,
                responsibilities,
                tone,
                additionalInfo
            })
        });

        const data = await response.json();
        
        if (data.error) {
            document.getElementById('result').innerHTML = `<p class="error">Error: ${data.error}</p>`;
        } else {
            document.getElementById('result').innerHTML = data.prompt;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

function copyToClipboard() {
    const result = document.getElementById('result');
    const text = result.innerText;
    navigator.clipboard.writeText(text).then(() => {
        const button = document.getElementById('copy-button');
        button.textContent = 'Copied!';
        setTimeout(() => {
            button.textContent = 'Copy to Clipboard';
        }, 2000);
    });
}
