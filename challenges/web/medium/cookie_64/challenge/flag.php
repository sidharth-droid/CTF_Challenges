<?php
error_reporting(0);
if (isset($_GET['debug']) && $_GET['debug'] === 'true') {
    highlight_file(__FILE__);
    exit();
}
if (!isset($_COOKIE['username'])) {
    header('Location: index.php');
}
$user = base64_decode($_COOKIE['username']);
if ($user === 'administrator') {
    include('safe.php');
    $flag = $safe_flag;
} else {
    $flag = "Hello <u>".htmlspecialchars($user)."</u>, you're not admin, no flag for you!";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Paradise - Flag Vault</title>
    <link rel="stylesheet" href="main.css">
</head>
<body>
    <div class="container">
        <div class="card flag-card">
            <h2 class="title">Flag Vault</h2>
            <div class="flag-box">
                <p><?php echo $flag; ?></p>
            </div>
            <!-- flag.php?debug=true -->
        </div>
    </div>
</body>
</html>