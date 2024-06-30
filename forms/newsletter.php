<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve the email from the form
    $email = $_POST['email'];

    // Your email address where the subscription notification will be sent
    $to = "mgasa.loucat1@gmail.com";

    // Email subject
    $subject = "New newsletter subscription";

    // Email message
    $message = "A new user has subscribed to your newsletter. Email: $email";

    // Additional headers
    $headers = "From: newsletter@example.com\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "Content-type: text/html\r\n";

    // Send email
    if (mail($to, $subject, $message, $headers)) {
        // If email is sent successfully, display a thank you message to the user
        echo "<h2>Thank you for subscribing!</h2>";
    } else {
        // If there's an error sending the email, display an error message
        echo "<h2>Sorry, there was an error processing your request. Please try again later.</h2>";
    }
}
?>
