import { send_api_request, toast_background, display_toast } from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('#removeFromCartBtn');
    buttons.forEach((button) => {
        button.addEventListener('click', remove_from_cart);
    });
})

async function remove_from_cart(event) {
    const clicked_button = event.currentTarget;
    const request_body = {
        cart_item_id: clicked_button.dataset.itemid
      }

    const response_data = await send_api_request('/remove_from_cart', request_body, 'DELETE');

    if (response_data.error) {
      display_toast('Error!', response_data.error, toast_background.ERROR);
    } else {
      display_toast('Success!', response_data.message, toast_background.SUCCESS);
    }
  
}


