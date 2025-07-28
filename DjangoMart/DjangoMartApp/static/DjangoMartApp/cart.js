import { getCSRFToken, toast_background, display_toast } from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('#removeFromCartBtn');
    buttons.forEach((button) => {
        button.addEventListener('click', remove_from_cart);
    });
})

async function remove_from_cart(event) {
    const clicked_button = event.currentTarget;
    try {
    const response = await fetch('/remove_from_cart', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({
        cart_item_id: clicked_button.dataset.itemid
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


