/**
 * @fileoverview Keep-alive request script for EasyConnect SOCKS5 node
 */
// cron: */5 * * * *
const url = "https://xxx.edu.cn/";
const method = "GET";
const headers = {"Content-Type": "application/json"};

const myRequest = {
    url: url,
    method: method, // Optional, default GET.
    headers: headers, // Optional.
};

function sendKeepAliveRequest() {
    $task.fetch(myRequest).then(response => {
        // Handle the response.
        console.log(`Status: ${response.statusCode}`);
        console.log(`Response: ${response.body}`);
        $notify("Keep-alive Request", "Success", `Status: ${response.statusCode}`); // Success notification.
        $done();
    }, reason => {
        // Handle the error.
        console.log(`Error: ${reason.error}`);
        $notify("Keep-alive Request", "Error", reason.error); // Error notification.
        $done();
    });
}

// Call the function to send the request.
sendKeepAliveRequest();
