<?php
$servername = "localhost";
$username = "root";
$password = "nothing";
$dbname = "db_robot";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " 
  . $conn->connect_error);
}

$sql = "SELECT motor1, motor2, motor3 , motor4 , motor5 , motor6 FROM motors";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    echo "motor1 " . $row["motor1"]. " motor2 " . $row["motor2"]. " motor3" . $row["motor3"]. "motor4" . $row["motor4"]. "motor5 " .
$row["motor5"]. "motor6"  . $row["motor6"].	"<br>";
  }
} else {
  echo "0 results";
}
$conn->close();
?>