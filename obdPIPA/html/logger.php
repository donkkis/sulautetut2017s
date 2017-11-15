<?php

session_start();

//check for existing session
if (isset($_POST["login"])){
	$_SESSION["user"] = $_POST["user"];
	$_SESSION["pw"] = $_POST["pw"];
}

$servername = "localhost";
$username = $_POST['user'];
$password = $_POST['pw'];
$dbname = "obdlogger";
// Create connection
$mysqli = new mysqli($servername, $_SESSION["user"], $_SESSION["pw"], $dbname);

//Check connection
if ($mysqli->connect_error) {
	die("Connection failed: " . $mysqli->connect_error);
}
?>
<body bgcolor="#767882">
<h1 align="center">OBD Logger</h1>
<p align="center">
<?php

//For getting the most recent location
$sq = "SELECT GPS_Lat, GPS_Long FROM Entry ORDER BY Timestamp DESC LIMIT 1";
$resu =  $mysqli->query($sq);
$row = $resu->fetch_assoc();
$lat = $row["GPS_Lat"];
$long = $row["GPS_Long"];

echo "<center>
	 <iframe src=
		\"https://www.google.com/maps/embed/v1/search?key=AIzaSyDllvM8JUZAhXK4iGI1inzBDv90IyCFdPo&q="
		.$lat.",".$long."\" 
		width=\"400\" 
		height=\"300\" 
		frameborder=\"0\" 
		style=\"border:0\" 
		allowfullscreen>
	</iframe>  
	</center></br>";

//Make another sql query
$sql = "SELECT * FROM Entry ORDER BY Timestamp DESC LIMIT 15";
$result =  $mysqli->query($sql);

if ($result->num_rows >  0) {
	echo "<center><table><tr>
			<th>Timestamp</th>
			<th>DeviceID</th>
			<th>GPS_Lat</th>
			<th>GPS_Long</th>
			<th>RPM</th>
			<th>Calc_load</th>
			<th>Speed</th>
		</tr>";
	//output data of each row
	while($row = $result->fetch_assoc()) {
		echo "<tr><td>".$row["Timestamp"].
			"</td><td>".$row["DeviceID"].
                        "</td><td>".$row["GPS_Lat"].
			"</td><td>".$row["GPS_Long"].
			"</td><td>".$row["RPM"].
			"</td><td>".$row["Calc_load"].
			"</td><td>".$row["Speed"].
			"</td></tr>";
	}
	echo "</table></center>";
} else {
	echo "0 results";
}
$mysqli->close();
 ?>
</p>
<p>
	<center>
		<a href="logout.php">Log out</a>
	</center>
</>
</body>
