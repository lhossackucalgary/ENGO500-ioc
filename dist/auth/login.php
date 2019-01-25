<?php
  $uname = $_POST['uname'];
  $pw = $_POST['passw'];

  $mysqli = new mysqli("127.0.0.1", "root", "pw", "Auth");
  if ($mysqli->connect_errno) {
    echo '{"Success": false}';
  }

  $stmt = $mysqli->prepare("SELECT * FROM Login WHERE email = ? AND password = ?");
  $stmt->bind_param("ss", $uname, $pw);
  $stmt->execute();
  $stmt->store_result();

  if ($stmt->num_rows() == 1) {
    echo '{"Success": true}';
  } else {
    echo '{"Success": false}';
  }

  $stmt->close();
?>
