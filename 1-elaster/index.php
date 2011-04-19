<!DOCTYPE html>
<?php
require_once('php/db_conn.php');
include('php/facebook_sdk.php');
$perms = 'user_events,create_event,rsvp_event';
$facebook = new Facebook(array(
  'appId'  => '208577865834024',
  'secret' => 'ba90c5d51930b3bfc651d0a1d6819884',
  'cookie' => true,
));
$session = $facebook->getSession();
$me = null;
if($session) {
  $uid = $facebook->getUser();
  $me = $facebook->api('/me');
}
?>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>地圖行事曆</title>
  <style type="text/css">
    #l {
      float: left;
    }
    #r {
      float: right;
    }
    #r div {
      margin-bottom: 20px;
    }
  </style>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.2/jquery.min.js"></script>
  <script type="text/javascript" src="http://connect.facebook.net/zh_TW/all.js"></script>
</head>
<body>
  <div id="fb-root">
    <div id="l">
    </div>
    <div id="r">
      <div><fb:login-button width="300" autologoutlink="true" perms="<?php echo $perms; ?>"></fb:login-button></div>
    <?php if($me): ?>
      <div>Hello, <?php echo $me['name']; ?>.</div>
    <?php endif ?>
      <div><fb:friendpile width="300" show-faces="true"></fb:friendpile></div>
      <div><fb:like-box width="300" href="http://www.facebook.com/apps/application.php?id=208577865834024" stream="false" header="false"></fb:like-box></div>
    </div>
  </div>
  <script type="text/javascript">
    FB.init({
      apiKey:   '8d955ca9f882c155282c7f3bbbda017c',
      appId:    '<?php echo $facebook->getAppId(); ?>',
      session:  <?php echo json_encode($session); ?>,
      status:   true,
      cookie:   true
    });
  <?php if(!$me): ?>
    FB.Event.subscribe('auth.login', function() { window.location.reload(); });
  <?php else: ?>
    FB.Event.subscribe('auth.logout', function() { window.location.reload(); });
  <?php endif ?>
    FB.XFBML.parse($('#r')[0]);
  </script>
</body>
</html>
