# def test_post_contact(client, mocker):
#     # Mock the send_email function
#     mock_send_email = mocker.patch(
#         "modules.contact_support.controller.contact_routes.resend_contact_sales_email"
#     )

#     # Define test data
#     test_data = {"customer_email": "test@example.com", "content": "Test message"}

#     # Call the endpoint
#     response = client.post("/contact", json=test_data)

#     # Assert that the response is as expected
#     assert response.status_code == 200

#     # Assert that send_email was called with the expected parameters
#     mock_send_email.assert_called_once()
