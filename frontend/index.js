async function sendFile() {
    const url = "http://127.0.0.1:5000/extract";
    const file = document.getElementById("file").files[0];

    const formData = new FormData();
    formData.append("file", file);

    console.log("Sending file...");

    const response = await fetch(url, {
        method: "POST",
        body: formData,
    });
}