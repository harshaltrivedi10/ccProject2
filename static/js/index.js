const submitRequest = (clickedButton, divID) => {
    setTimeout(() => {
        var item = document.getElementById(divID);
        if (item) {
            if(item.className=='btn btn-secondary hidden'){
                item.className = 'btn btn-secondary unhidden' ;
                clickedButton.value = 'hide';
            }else{
                item.className = 'btn btn-secondary hidden';
                clickedButton.value = 'unhide';
            }
        }
    }, 1000);
}
