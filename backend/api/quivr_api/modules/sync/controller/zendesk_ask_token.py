zendeskAskTokenPage = """
<!DOCTYPE html>
<html>
<head>
    <title>Enter Zendesk API Token</title>
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
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .input-field {
            margin-bottom: 20px;
        }
        .submit-button {
            padding: 10px 20px;
            font-size: 1em;
            color: #fff;
            background-color: #6142d4;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .submit-button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Enter Your Zendesk API Token</h2>
        <form action="/sync/zendesk/submit-token" method="post">
            <div class="input-field">
                <input type="text" name="api_token" placeholder="API Token" required>
            </div>
            <button type="submit" class="submit-button">Submit</button>
        </form>
    </div>
</body>
</html>
"""
