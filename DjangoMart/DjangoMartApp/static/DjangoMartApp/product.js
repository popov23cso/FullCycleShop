import { toast_background, display_toast, adjust_int_value_by_id, send_api_request } from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#addToCartBtn').addEventListener('click', add_to_cart);
})


async function add_to_cart() {
  const product_id = document.querySelector('#productId').value;
  const quantity = parseInt(document.querySelector('#quantity').value, 10);
  const request_body = {
      product_id: product_id,
      quantity: quantity
  }

  const response_data = await send_api_request('/add_to_cart', request_body, 'POST');
  
  if (response_data.error) {
    display_toast('Error!', response_data.error, toast_background.ERROR);
  } else {
    display_toast('Success!', response_data.message, toast_background.SUCCESS);
    adjust_int_value_by_id(quantity, 'cartItemsCount');
  }

}


