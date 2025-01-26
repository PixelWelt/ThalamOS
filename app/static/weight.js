async function getWeight() {
    document.getElementById("scaleButton").disabled = true;
    try {
        const response = await fetch(`${API_URL}/wifiscale/weight`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        sendLog('info', `Weight data: ${JSON.stringify(data)}`);

        const pairs = document.getElementsByClassName("pair");
        const lastPair = pairs[pairs.length - 1];
        if (lastPair.children[0].value !== "" && lastPair.children[1].value !== "") {
            addPairInput();
        }

        const newPair = pairs[pairs.length - 1];
        newPair.children[0].value = "weight";
        newPair.children[1].value = data["weight"];
    } catch (error) {
        sendLog('error', `Error fetching weight: ${error}`);
    } finally {
        document.getElementById("scaleButton").disabled = false;
    }
}
