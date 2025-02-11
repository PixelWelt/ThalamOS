async function sendLog(level, message) {
    try {
        await fetch(`${API_URL}/log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ level: level, message: message })
        });
    } catch (error) {
        console.error('Error sending log:', error);
    }
}
