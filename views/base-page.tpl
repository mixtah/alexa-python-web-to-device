%setdefault('page','home')
%setdefault('alert','')
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="A Simple Message Board">
	<meta name="author" content="Michael Bauer">
	<title>RedSun</title>
	<!-- CSS Styles -->
	<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
	<!-- Theme -->
	<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous">
	<link rel="stylesheet" type="text/css" href="/styles/styles.css">
	<!-- JS Scripts -->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
</head>
<body>
<nav class="navbar navbar-default">
	<div class="container-fluid">
		<div class="navbar-header">
			<a class="navbar-brand" href="/">RedSun</a>
		</div>
		<ul class="nav navbar-nav">
		</ul>
	</div>
</nav>

	<div class="container" style="margin-top:0px">
		
		%if len(alert)>0:
			<div class="alert alert-warning" role="alert">
			    <p align="center"><b>{{!alert}}</b></p>
			</div>
		%end
		
    	{{!base}}
    </div>

	<div class="container">
	    <footer>
	    	<br><br>
	        <h4 style="color:#656565;text-align: center;">Created by That-VR-Team @ NASA SpaceApps Hackathon Sydney</h4>
	    </footer>
	</div>
</body>

</html>