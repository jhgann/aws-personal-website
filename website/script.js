window.onload = function loadVisitCount() {
    var apiCountUrl = "https://csiozy6n1g.execute-api.us-east-1.amazonaws.com/Prod/count"
    fetch(apiCountUrl, {
        method: 'POST'
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('Success: visitcount = ', data);
        document.getElementById("visitcount").innerHTML = data;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
};