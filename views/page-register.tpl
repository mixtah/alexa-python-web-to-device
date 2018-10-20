%rebase("base-page")


<p>Got these details: {{oauth_vars}}</p>

<p>Enter click on the link below and enter this code
<a href="{{oauth_vars.get('verification_uri','#')}}" target="_blank">Click here to register this device</a>
