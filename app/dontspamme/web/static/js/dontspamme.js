var dontspamme = new Object();

/* Check if the 'email' is well constructed
 * http://stackoverflow.com/questions/46155/validate-email-address-in-javascript
 */
dontspamme.isValidEmail = function(email){    
    return email.match(
         /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    )
};