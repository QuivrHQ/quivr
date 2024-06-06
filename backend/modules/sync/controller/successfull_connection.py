successfullConnectionPage = """
<!DOCTYPE html>
<html>
<head>
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
        .close-button {
            padding: 10px 20px;
            font-size: 1em;
            color: #fff;
            background-color: #007bff;
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
        <div class="message">Connection Successful!</div>
        <button class="close-button" onclick="window.close();">Close Tab</button>
    </div>
</body>
</html>
"""