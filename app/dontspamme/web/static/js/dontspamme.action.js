dontspamme.action = new Object();

dontspamme.action.confirm = function(confirmMessage){
    if(confirm("Are you sure you want to " + confirmMessage + "?")){
        document.confirmation.submit();
    } else {
        window.location = '/';
    }
};