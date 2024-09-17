let stripe, elements;
const stripeSubmit = document.getElementById('stripe-submit');

// Function to create a Stripe session
async function createStripeSession() {

  // Switch the payment method to Stripe
  switchPaymentMethod('stripe', '');

  const form = document.getElementById('form-user-info');
  const formData = new FormData(form);

  // Disable the submit button while processing
  stripeSubmit.disabled = true;
  try {
    // Make a POST request to create a Stripe session
    const { data } = await axios.post("/checkout/stripe", formData);
    const { client_secret } = data;

    const appearance = { theme: 'flat' }; // Customize the appearance of the Stripe elements
    elements = stripe.elements({ appearance, clientSecret: client_secret });
    const paymentElement = elements.create("payment");
    paymentElement.mount("#payment-element");

    // Add event listener to handle the form submission
    document
      .querySelector("#payment-form")
      .addEventListener("submit", _stripeFormSubmit);

    // Display the Stripe card input field
    document.getElementById('stripe-card').style.display = 'block';
    stripeSubmit.disabled = false; // Enable the submit button again
  } catch (e) {
    console.log(e);
    notyf.error(e.response.data.message); // Show error notification if there's an issue
  }
}

// Function to handle Stripe form submission
async function _stripeFormSubmit(e) {
  e.preventDefault(); // Prevent the default form submission behavior
  stripeSubmit.disabled = true;

  const host = window.location.protocol + "//" + window.location.host; // Get the host for redirecting

  // Confirm payment with Stripe
  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: `${host}/checkout/complete`, // Redirect URL after payment
    },
  });

  // Handle card or validation errors
  if (error.type === "card_error" || error.type === "validation_error") {
    notyf.error(error.message);
  } else {
    notyf.error("Sorry, something went wrong during the payment process."); // General error message
  }
  stripeSubmit.disabled = false; // Enable the submit button again
}

// Function to check Stripe payment status
async function _checkStripePaymentStatus() {
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );
  if (!clientSecret) {
    return;
  }

  // Retrieve the payment intent status
  const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);
  switch (paymentIntent.status) {
    case "succeeded":
      notyf.success("Payment has been successfully completed!"); // Success message
      break;
    case "processing":
      notyf.success("Payment is being processed."); // Processing message
      break;
    default:
      notyf.error("Sorry, something went wrong during the payment process."); // General error message
      break;
  }
}

// Function to initialize Stripe
async function _stripeInit() {
    const { data } = await axios("/checkout/stripe/config");
    stripe = Stripe(data.public_key, { locale: 'en' }); // Initialize Stripe with the public key and set the locale to English
    _checkStripePaymentStatus(); // Check the payment status on load
}

// Initialize Stripe
_stripeInit();

