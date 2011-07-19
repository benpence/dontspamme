dontspamme.page = new Object();

/* Get variable from javascript prompt */
dontspamme.page.submitByPrompt = function(formNode, variableName){
    var message = variableName.charAt(0).toUpperCase() + variableName.slice(1) + ':';
    
    var value = prompt(message);
    
    if(value == null && value == ""){
        return
    }
    
    formNode[variableName].value = value;
    formNode.submit();
};

/* Choose variable value based on click in form */
dontspamme.page.submitWithValue = function(formNode, variableName, value){
    // This should never be true
    if(value == null && value == ""){
        return
    }
    
    formNode[variableName].value = value;
    formNode.submit();
};

/* Checks if non-empty field and submits */
dontspamme.page.submitText = function(formNode){
    if(formNode.firstChild.value != ''){
        formNode.submit();
    }
};