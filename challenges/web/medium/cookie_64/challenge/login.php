<?php
error_reporting(0);
$users = [
    'guest' => 'guest',
    'admin' => '2YvNatBCgPqSMSxdfJQCtPaBhev499SX'
];

if (isset($_POST['username']) && isset($_POST['password']) && is_string($_POST['username']) && is_string($_POST['password'])) {
    $u = $_POST['username'];
    $p = $_POST['password'];
    error_log("[login.php] Tried login with [$u, $p]\n", 3, "../logs/stats.log");
    if (array_key_exists($u, $users) && $users[$u] === $p) {
        setcookie("username", base64_encode($u), time() + 3600);
        Header('Location: flag.php');
    } else {
        Header('Location: index.php?error=Invalid credentials');
    }
} else {
    Header('Location: index.php?error=Username and password required');
}