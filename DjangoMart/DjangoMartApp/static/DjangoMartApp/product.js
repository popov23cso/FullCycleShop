document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#addToCartBtn').addEventListener('click', add_to_cart);
})

const toast_background = {
  ERROR: 'text-bg-danger',
  SUCCESS: 'text-bg-success',
};

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

function display_toast(message, body, background) {
    const toast_element = document.querySelector('#liveToast');
    const toast_message = document.querySelector('#toastMessage');
    const toast_body = document.querySelector('#toastBody');

    toast_element.classList.remove(toast_background.SUCCESS, toast_background.ERROR);
    toast_element.classList.add(background);

    toast_message.innerText = message;
    toast_body.innerText = body;

    const toast = new bootstrap.Toast(toast_element);
    toast.show();
}

function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}

