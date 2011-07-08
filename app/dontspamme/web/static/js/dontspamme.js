var dontspamme = new Object();

dontspamme.checkDomain = function(formNode){
    var textNode = formNode.firstChild;
    
    if(textNode.value != ''){
        formNode.submit();
    }
}

dontspamme.removeDomain = function(formNode, domain_name){
    formNode['domain'].value = domain_name;
    formNode.submit();
}