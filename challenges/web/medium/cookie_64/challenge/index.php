<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Paradise - Login</title>
    <link rel="stylesheet" href="main.css">
</head>
<body>
    <div class="container">
        <div class="card">
            <h2 class="title">Paradise Access Terminal</h2>
            <form action="login.php" method="POST">
                <div class="input-group">
                    <label class="label">Username</label>
                    <input type="text" name="username" id="username" class="form-control" placeholder="Enter username" />
                </div>
                <div class="input-group">
                    <label class="label">Password</label>
                    <input type="password" name="password" id="password" class="form-control" placeholder="Enter password" />
                </div>
                <button type="submit" class="btn">Access System</button>
                <?php if(isset($_GET['error'])) : ?>
                    <div class="error"><?php echo htmlspecialchars($_GET['error']); ?></div>
                <?php endif; ?>
            </form>
        </div>
    </div>
    <!--TODO remove user guest:guest in production -->
</body>
</html>