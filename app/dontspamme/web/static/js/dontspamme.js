var dontspamme = new Object();

dontspamme.checkDomain = function(formNode){
    var textNode = formNode.firstChild;
    
    if(textNode.value != ''){
        formNode.submit();
    }
}

dontspamme.addDomain = function(formNode){
    var domain = prompt("Add domain:")
    
    if(domain == null && domain == ""){
        return
    }
    
    formNode['domain'].value = domain;
    formNode.submit();
}

dontspamme.removeDomain = function(formNode, domain){
    formNode['domain'].value = domain;
    formNode.submit();
}