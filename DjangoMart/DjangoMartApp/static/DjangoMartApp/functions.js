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