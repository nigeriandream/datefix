<!DOCTYPE html>
<html dir="ltr" lang="en-US">

<head>

	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<meta name="author" content="SemiColonWeb" />

	<!-- Stylesheets
	============================================= -->
	<link href="https://fonts.googleapis.com/css?family=Lato:300,400,400i,700|Raleway:300,400,500,600,700|Crete+Round:400i" rel="stylesheet" type="text/css" />
	<link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700|Roboto:300,400,500,700" rel="stylesheet" type="text/css" />
	<link rel="stylesheet" href="css/bootstrap.css" type="text/css" />
	<link rel="stylesheet" href="css/style.css" type="text/css" />
	<link rel="stylesheet" href="css/dark.css" type="text/css" />
	<link rel="stylesheet" href="css/font-icons.css" type="text/css" />
	<link rel="stylesheet" href="css/et-line.css" type="text/css" />
	<link rel="stylesheet" href="css/animate.css" type="text/css" />
	<link rel="stylesheet" href="css/magnific-popup.css" type="text/css" />

	<link rel="stylesheet" href="css/fonts.css" type="text/css" />

	<link rel="stylesheet" href="css/responsive.css" type="text/css" />
	<meta name="viewport" content="width=device-width, initial-scale=1" />

	<!-- Document Title
	============================================= -->
	<title>Datefix | Login</title>

</head>

<body class="stretched">

	<!-- Document Wrapper
	============================================= -->
	<div id="wrapper" class="clearfix">

		<!-- Top Bar
		============================================= -->

		<!-- Header
		============================================= -->
		<header id="header" class="full-header">

			<div id="header-wrap">

				<div class="container clearfix">

					<div id="primary-menu-trigger"><i class="icon-reorder"></i></div>

					<!-- Logo
					============================================= -->
					<div id="logo">
						<a href="index.php" class="standard-logo" data-dark-logo="images/logo-dark.png"><img src="images/logo.png" alt="Canvas Logo"></a>
						<a href="index.php" class="retina-logo" data-dark-logo="images/logo-dark@2x.png"><img src="images/logo@2x.png" alt="Canvas Logo"></a>
					</div><!-- #logo end -->

					<!-- Primary Navigation
					============================================= -->
					<nav id="primary-menu">

						<ul class="one-page-menu" data-easing="easeInOutExpo" data-speed="1250" data-offset="65">
							<li><a href="index.php">
									<div>Home</div>
								</a>
							</li>
							<li><a href="#">
									<div>About Datefix</div>
								</a>
							</li>
						</ul>


					</nav><!-- #primary-menu end -->

				</div>

			</div>

		</header><!-- #header end -->

		<!-- Page Title
		============================================= -->
		<section id="page-title">

			<div class="container clearfix">
				<h1>My Account</h1>
				<ol class="breadcrumb">
					<li class="breadcrumb-item"><a href="index.php">Datefix</a></li>
					<li class="breadcrumb-item active" aria-current="page">Login</li>
				</ol>
			</div>

		</section><!-- #page-title end -->

		<!-- Content
		============================================= -->
		<section id="content">

			<div class="content-wrap">

				<div class="container clearfix">

					<div class="col_one_third nobottommargin">

						<div class="well well-lg nobottommargin">
							<form id="login-form" name="login-form" class="nobottommargin" action="#" method="post">

								<h3>Login to your Account</h3>

								<div class="col_full">
									<label for="email">Email Address:</label>
									<input type="text" id="email" name="email" value="" class="form-control" />
								</div>

								<div class="col_full">
									<label for="password">Password:</label>
									<input type="password" id="password" name="password" value="" class="form-control" />
								</div>

								<div class="col_full nobottommargin">
									<button class="button button-3d nomargin" id="submit" name="submit" value="login">Login</button>
									<a href="#" class="fright">Forgot Password?</a>
								</div>

							</form>
						</div>

					</div>

					<div class="col_two_third col_last nobottommargin">


						<h3>Don't have an Account? Register Now.</h3>

						<form id="register-form" name="register-form" class="nobottommargin" action="#" method="post">

							<div class="col_half">
								<label for="first-name">First Name:</label>
								<input type="text" id="first-name" name="first-name" value="" class="form-control" />
							</div>

							<div class="col_half col_last">
								<label for="last-name">Last Name:</label>
								<input type="text" id="last-name" name="last-name" value="" class="form-control" />
							</div>

							<div class="clear"></div>

							<div class="col_half">
								<label for="email">Email Address:</label>
								<input type="text" id="email" name="email" value="" class="form-control" />
							</div>

							<div class="col_half col_last">
								<label for="phone">Phone Number:</label>
								<input type="text" id="phone" name="phone" value="" class="form-control" />
							</div>

							<div class="clear"></div>

							<div class="col_half">
								<label for="sex">Sex:</label>
								<select name="sex" id="sex" class="form-control">
									<option value="" selected="selected" disabled></option>
									<option value="male">Male</option>
									<option value="female">Female</option>
								</select>
							</div>

							<div class="col_half col_last">
								<label for="register-form-phone">Looking For:</label>
								<select name="partner-sex" id="partner-sex" class="form-control">
									<option value="" selected="selected" disabled></option>
									<option value="male">Male</option>
									<option value="female">Female</option>
								</select>
							</div>

							<div class="clear"></div>

							<div class="col_half">
								<label for="password">Choose Password:</label>
								<input type="password" id="password" name="register-form-password" value="" class="form-control" />
							</div>

							<div class="col_half col_last">
								<label for="repassword">Re-enter Password:</label>
								<input type="password" id="repassword" name="repassword" value="" class="form-control" />
							</div>


							<div class="col_full nobottommargin">
								<button class="button button-3d button-black nomargin" id="register-form-submit" name="register-form-submit" value="register">Register Now</button>
							</div>

						</form>

					</div>

				</div>

			</div>

		</section><!-- #content end -->

		<!-- Footer
		============================================= -->
		<?php include_once 'footer.php'; ?>
		<!-- #footer end -->

	</div><!-- #wrapper end -->

	<!-- Go To Top
	============================================= -->
	<div id="gotoTop" class="icon-angle-up"></div>

	<!-- External JavaScripts
	============================================= -->
	<script src="js/jquery.js"></script>
	<script src="js/plugins.js"></script>
	<script src="js/select2.js"></script>
	<script src="js/conditional-form.js"></script>
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
	<script src="js/msform.js"></script>

	<!-- Footer Scripts
	============================================= -->
	<script src="js/functions.js"></script>

</body>

</html>