const submitRequest = (fileName) => {
    console.log(fileName)
    var userName = document.querySelector("#personName").value;
    console.log(userName);
    var request = new XMLHttpRequest()
    request.open('POST', 'http://127.0.0.1:5000/uploadFile?fileName='+fileName+'&userName='+userName, true)
    request.onload = function() {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response);
        console.log("Initial request successful");
        console.log(data);
    }
    request.send();
    // setTimeout(() => {
    //     var item = document.getElementById(divID);
    //     if (item) {
    //         if(item.className=='btn btn-secondary hidden'){
    //             item.className = 'btn btn-secondary unhidden' ;
    //             clickedButton.value = 'hide';
    //         }else{
    //             item.className = 'btn btn-secondary hidden';
    //             clickedButton.value = 'unhide';
    //         }
    //     }
    // }, 1000);
}

