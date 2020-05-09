const submitRequest = (fileName, userName, host) => {

    var request = new XMLHttpRequest()
    console.log(host)
    request.open('POST', '/uploadFile?fileName='+fileName+'&userName='+userName, true)
    request.onload = function() {
        var data = JSON.parse(this.response);
        console.log("Initial request successful");
        console.log(data);
    }
    request.send();
}

const identifyAndGeneratePerformanceReport = (fileName) => {
    var request = new XMLHttpRequest();
    request.open('POST', '/identifyUser?fileName='+fileName, true);
    request.onload = function () {
        var data = JSON.parse(this.response);
        console.log('Request to identify user handled successfully!');
        console.log(data);
    }
    request.send()
}

const generateAndDownloadReport = () => {
    var request = new XMLHttpRequest();
    request.open('GET', '/generateAndDownloadReport', true);
    request.onload = function () {
        // var data = JSON.parse(this.response);
        console.log('Initial request handled successfully!');
        // console.log(data);
    }
    request.send()
}