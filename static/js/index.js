const submitRequest = (fileName, userName, host) => {
    // console.log(fileName)
    // console.log(userName);
    var request = new XMLHttpRequest()
    console.log(host)
    request.open('POST', host+'/uploadFile?fileName='+fileName+'&userName='+userName, true)
    request.onload = function() {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response);
        console.log("Initial request successful");
        console.log(data);
    }
    request.send();
}

const identifyAndGeneratePerformanceReport = (fileName,  host) => {
    // let classes = document.querySelector("#getReports").classList;
    // console.log(typeof (classes));
    // if (!classes.contains('hidden')) {
    //     document.querySelector("#getReports").classList.add("hidden");
    // } else {
    //     document.querySelector("#getReports").classList.remove("hidden");
    // }
    console.log(host)
    var request = new XMLHttpRequest();
    request.open('POST', host+'/identifyUser?fileName='+fileName, true);
    request.onload = function () {
        var data = JSON.parse(this.response);
        console.log('Request to identify user handled successfully!');
        console.log(data);
    }
    request.send()
}

const generateAndDownloadReport = (host) => {
    console.log(host)
    var request = new XMLHttpRequest();
    request.open('GET', host+'/generateAndDownloadReport', true);
    request.onload = function () {
        // var data = JSON.parse(this.response);
        console.log('Initial request handled successfully!');
        // console.log(data);
    }
    request.send()
}