<?php
  $uname = $_GET['uname'];
  $pw = $_GET['passw'];

  $mysqli = new mysqli("127.0.0.1", "root", "pw", "Auth");
  if ($mysqli->connect_errno) {
    echo '{"Success": false, "iot_id": null}';
  }

  $stmt = $mysqli->prepare("SELECT iot_id FROM Login WHERE email = ? AND password = ?");
  $stmt->bind_param("ss", $uname, $pw);
  $stmt->execute();
  $stmt->store_result();

  if ($stmt->num_rows() == 1) {
    $stmt->bind_result($iot_id);
    $stmt->fetch();
    echo '{"Success": true, "iot_id":' . $iot_id . '}';
  } else {
    echo '{"Success": false, "iot_id": null}';
  }

  $stmt->close();
?>
