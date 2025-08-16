export function getCSRFToken() {
  return document.cookie
  .split('; ')
  .find(row => row.startsWith('csrftoken='))
  ?.split('=')[1];
}


export const toast_background = {
  ERROR: 'text-bg-danger',
  SUCCESS: 'text-bg-success',
};


export function display_toast(message, body, background) {
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


export function adjust_int_value_by_id(change_ammount, element_id) {
  const element = document.querySelector('#' + element_id);
  element.innerText = parseInt(element.innerText, 10) + change_ammount;
}

export function hide_element(selector) {
  const element = document.querySelector(selector);
  element.style.display = 'none';
}

export function show_element(selector) {
  const element = document.querySelector(selector);
  element.style.display = 'block';
}

export async function send_api_request(url, request_body) {
    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify(request_body)
        });
        return await response.json();
    } catch (err) {
        console.error('Fetch error:', err);
        display_toast('Error!', 'Something went wrong', toast_background.ERROR);
        return { error: true };
    }
}