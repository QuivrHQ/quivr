successfullConnectionPage = """
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f8f9fa;
            font-family: Arial, sans-serif;
        }
        .container {
            text-align: center;
        }
        .message {
            font-size: 2em;
            margin-bottom: 20px;
        }
        .icon {
            font-size: 2em;
            color: white;
            background-color: green;
            border-radius: 50%;
            padding: 20px;
            margin-bottom: 20px;
        }
        .close-button {
            padding: 10px 20px;
            font-size: 1em;
            color: #fff;
            background-color: #6142d4;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .close-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <i class="fas fa-check icon"></i>
        <div class="message">Connection successful</div>
        <button class="close-button" onclick="window.close();">Close Tab</button>
    </div>
</body>
</html>
"""