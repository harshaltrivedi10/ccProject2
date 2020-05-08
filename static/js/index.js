const submitRequest = (fileName, userName) => {
    // console.log(fileName)
    // console.log(userName);
    var request = new XMLHttpRequest()
    
    request.open('POST', 'https://cse546-final.uc.r.appspot.com/uploadFile?fileName='+fileName+'&userName='+userName, true)
    request.onload = function() {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response);
        console.log("Initial request successful");
        console.log(data);
    }
    request.send();
}

const identifyAndGeneratePerformanceReport = (fileName) => {
    // let classes = document.querySelector("#getReports").classList;
    // console.log(typeof (classes));
    // if (!classes.contains('hidden')) {
    //     document.querySelector("#getReports").classList.add("hidden");
    // } else {
    //     document.querySelector("#getReports").classList.remove("hidden");
    // }

    var request = new XMLHttpRequest();
    request.open('POST', 'https://cse546-final.uc.r.appspot.com/identifyUser?fileName='+fileName, true);
    request.onload = function () {
        var data = JSON.parse(this.response);
        console.log('Request to identify user handled successfully!');
        console.log(data);
    }
    request.send()
}

const generateAndDownloadReport = () => {
    var request = new XMLHttpRequest();
    request.open('GET', 'https://cse546-final.uc.r.appspot.com/generateAndDownloadReport', true);
    request.onload = function () {
        // var data = JSON.parse(this.response);
        console.log('Initial request handled successfully!');
        // console.log(data);
    }
    request.send()
}