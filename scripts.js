// scripts.js

document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');

    // Function to handle button clicks
    async function handleButtonClick(event) {
        const buttonId = event.target.id;

        try {
            const response = await fetch('http://127.0.0.1:5000/run-python', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: buttonId }),
                mode: 'cors'
            });

            if (!response.ok) {
                throw new Error(`Network response was not ok. Status: ${response.status}, StatusText: ${response.statusText}`);
            }

            const result = await response.json();
            if (typeof result.result === 'object' && result.result !== null) {
                output.innerHTML = `
                    <p>Question: ${result.result.question_name}</p>
                    <p>Difficulty: ${result.result.difficulty}</p>
                    <p>Status: ${result.result.status}</p>
                    <p>URL: <a href="${result.result.question_url}" target="_blank">${result.result.question_url}</a></p>
                `;
            } else {
                output.textContent = result.result;
            }
        } catch (error) {
            console.error('Fetch error:', error);
            output.textContent = 'Error: ' + error.message;
        }
    }

    // Adding event listeners to buttons
    const buttons = document.querySelectorAll('.ref');
    buttons.forEach(button => {
        button.addEventListener('click', handleButtonClick);
    });
});
