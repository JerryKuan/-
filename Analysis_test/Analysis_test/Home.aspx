<%@ Page Language="vb" AutoEventWireup="false" CodeBehind="Home.aspx.vb" Inherits="Analysis_test.Home" %>


<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
		
	<title>Single Page Responsive Portfolio Site - Tenero</title>
	
	<meta name="description" content="A free single page responsive portfolio website html template for designers, developers and entrepreneurs.">
	<meta name="keywords" content="responsive, free, html, template">
	
    <script src="js/jquery.min.js"></script>
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
	
	<!-- Stylesheets -->
	
	<link rel="stylesheet" href="styles/essentials.css">
	<link rel="stylesheet" href="styles/font-awesome.min.css">
	<link rel="stylesheet" href="styles/jquery.bxslider.css">
	
	<!-- Main stylesheet -->
	<link rel="stylesheet" href="styles/style.css">
	<link rel="stylesheet" href="styles/color.css">
	
	<!-- Favicon -->
	<link rel="shortcut icon" href="images/favicon.ico">
	<style>
     .user-form{
         width:300px;
         margin:0 auto;
     }
     input[type="password"]{
         height:40px;
     }
	</style>
</head>


<body >
	<section id="home" class="home-wrap">
		<div class="home-content text-white">
			<h1 class="bigtext letterspace uppercase bold no-margin">Analyis result dispaly</h1>
            <div class="user-form">
                <div><input type="text" id="username" name="username" placeholder="username" /></div>
                <div><input class="user-form" id="userpass" type="password" name="userpass" placeholder="password" /></div>
            </div>
			<p><a class="button outline fill white big smoothscroll" onclick="submit();">go to view result</a></p>
		</div>
	</section>

	<div style="background-image: url('images/studio.jpg');margin-top:45px;" class="fullscreen-img"></div>

</body>
<script>
    function submit() {
        //alert($("#username").val());
        if ($("#username").val() == "admin" && $("#userpass").val() == "admin") {
            location.href = "./Display.aspx";
        } else {
            alert("error user name or password");
        }
    }
</script>

</html>

