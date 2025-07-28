import { getCSRFToken, toast_background, display_toast } from './functions.js';

document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#addToCartBtn').addEventListener('click', add_to_cart);
})


async function add_to_cart() {
    const product_id = document.querySelector('#productId').value;
    const quantity = document.querySelector('#quantity').value;

    try {
    const response = await fetch('/add_to_cart', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({
        product_id: product_id,
        quantity: quantity
      })
    });

    const data = await response.json();
  
    if (data.error) {
      display_toast('Error!', data.error, toast_background.ERROR);
    } else {
      display_toast('Success!', data.message, toast_background.SUCCESS);
    }
  } catch (err) {
    console.error('Fetch error:', err);
    alert('Something went wrong.');
  }
}

