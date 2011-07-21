var dontspamme = Object();

dontspamme.ajaxCallback = function(method_type, url, data, callback, timeout, error_callback){
    if(!timeout){
        timeout = 0.125;
    }
    
    $.ajax({
        dataType: 'json',
        crossDomain: true,
        
        url: 'https://' + appID + '.appspot.com/api/',
        type: method_type,
        timeout: timeout * 2000,
      
        data: data,
        
        success: callback(data),
        error: error_callback,
    });
};