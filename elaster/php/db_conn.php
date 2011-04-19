<?php
  $DB_HOST        = "192.168.200.136:31309";
  $DB_USER        = "datemap_user";
  $DB_PASSWORD    = "datemap_celia";
  $DB_NAME        = "datemap_db";

  $conn = mysql_connect($DB_HOST, $DB_USER, $DB_PASSWORD);
  if (!$conn) {
	echo mysql_error($conn)."<br />";
	return;
  }
  if (!mysql_select_db($DB_NAME)) {
	echo mysql_error($conn)."<br />";
	return;
  }
  mysql_set_charset('utf8', $conn);
?>
