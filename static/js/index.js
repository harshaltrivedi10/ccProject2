const submitRequest = (fileName, userName) => {
    // console.log(fileName)
    // console.log(userName);
    var request = new XMLHttpRequest()
    request.open('POST', 'http://127.0.0.1:5000/uploadFile?fileName='+fileName+'&userName='+userName, true)
    request.onload = function() {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response);
        console.log("Initial request successful");
        console.log(data);
    }
    request.send();
}

const identifyAndGeneratePerformanceReport = () => {
    let classes = document.querySelector("#getReports").classList;
    // console.log(typeof (classes));
    if (!classes.contains('hidden')) {
        document.querySelector("#getReports").classList.add("hidden");
    }
    else {
        document.querySelector("#getReports").classList.remove("hidden");
    }
}

