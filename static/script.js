function joinQueue() {
    let name = document.getElementById("name").value;
    let service = document.getElementById("service").value;

    fetch("/join", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, service})
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerHTML =
            `Token: ${data.token}, Wait: ${data.wait_time} mins`;
    });
}