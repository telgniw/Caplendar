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
  try {
    $uid = $facebook->getUser();
    $me = $facebook->api('/me');
  } catch (FacebookApiException $e) {
    error_log($e);
  }
}
?>
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>地圖行事曆</title>
  <link rel="stylesheet" href="/css/style.css">
  <link rel="stylesheet" href="/css/cupertino/jquery-ui-1.8.11.custom.css">	
  <script type="text/javascript" src="/js/jquery-1.5.1.min.js"></script>
  <script type="text/javascript" src="/js/jquery-ui-1.8.11.custom.min.js"></script>
</head>
<body>
  <script type="text/javascript">
    $('#fb-root').ready(function() {
      $.getScript('http://connect.facebook.net/zh_TW/all.js', function() {
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
        $('.xfbml').each(function() {
          FB.XFBML.parse(this);
        });
      });
      $('#accordion').accordion({
        fillSpace: true
      });
      $('.accordion-content div').each(function() {
        $(this).css('margin-bottom', '20px');
      });
    });
  </script>
  <div id="fb-root">
    <div id="l">
      <?php if($me): ?>
      <span>Hello, <?php echo $me['name']; ?>.</span>
      <?php endif ?>
    </div>
    <div id="r">
      <div id="accordion">
        <div class="accordion-item">
          <h3><a href="#">主選單</a></h3>
          <div class="accordion-content">
            <div class="xfbml"><fb:login-button width="250" autologoutlink="true" perms="<?php echo $perms; ?>"></fb:login-button></div>
            <div class="xfbml"><fb:friendpile width="250" show-faces="true"></fb:friendpile></div>
            <div class="xfbml"><fb:like-box width="250" href="http://www.facebook.com/apps/application.php?id=208577865834024" stream="false" header="false"></fb:like-box></div>
          </div>
        </div>
        <?php if($me): ?>
        <div class="accordion-item">
          <h3><a href="#">行事曆</a></h3>
          <div class="accordion-content">
            <span>Haha!</span>
          </div>
        </div>
        <div class="accordion-item">
          <h3><a href="#">選項</a></h3>
          <div class="accordion-content">
            <span>Hello World!</span>
          </div>
        </div>
        <?php endif ?>
      </div>
    </div>
  </div>
</body>
</html>
