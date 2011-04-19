<?php
$GLOBAL_ERROR   = null;
$DB_HOST        = "192.168.200.136:31309";
$DB_USER        = "datemap_user";
$DB_PASSWORD    = "datemap_celia";
$DB_NAME        = "datemap_db";

$conn = mysql_connect($DB_HOST, $DB_USER, $DB_PASSWORD);
if(!$conn) {
  $GLOBAL_ERROR = mysql_error($conn);
  return;
}
if(!mysql_select_db($DB_NAME)) {
  $GLOBAL_ERROR = mysql_error($conn);
  return;
}
mysql_set_charset('utf8', $conn);
function insert($token, $uid, $name, $profile) {
  $query = "INSERT user (access_token, uid, name, profile_id, created) ".
    "VALUES ('$token', '$uid', '$name', '$profile', CURRENT_DATE()) ".
    "ON DUPLICATE KEY UPDATE ".
    "access_token='$token', uid='$uid', name='$name', profile_id='$profile';";
}
?>
