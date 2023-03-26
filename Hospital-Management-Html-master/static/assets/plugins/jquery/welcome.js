<><div id="displayName"></div><script type="text/javascript">
    var clientContext = new SP.ClientContext(_spPageContextInfo.webServerRelativeUrl);
    var user = clientContext.get_web().get_currentUser();
    clientContext.load(user);

    clientContext.executeQueryAsync(onUserNameSuccess, onUserNameFail);
    function onUserNameSuccess() {document.getElementById("displayName").innerText = "Welcome, " + user.get_title()};
    //To display last name first and for cases where full name consists of only two words.
    //var userToken = user.get_title().split(' ');
    //document.getElementById("displayName").innerText = "Welcome, " + userToken[1] + " " + userToken[0];

    {"}"}

    function onUserNameFail(args) {document.getElementById("displayName").innerText = 'Error:' + args.get_message()};
    {"}"}
//recommended to use ExecuteOrDelayUntilScriptLoaded on sp.js
</script></>