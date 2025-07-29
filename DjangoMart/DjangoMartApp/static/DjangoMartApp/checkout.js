import { getCSRFToken, toast_background, display_toast} from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
  document.querySelector('#saveAddressBtn').addEventListener('click', save_address);
})



async function save_address() {
    const city = document.getElementById('dropdownCity').value;
    const street = document.getElementById('dropdownStreet').value;
    const street_number = document.getElementById('dropdownStreetNumber').value;
    const phone_number = document.getElementById('dropdownPhoneNumber').value;

    try {
        const response = await fetch ('/add_address', {
            method: 'PUT',
            headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({
                city: city,
                street: street,
                street_number: street_number,
                phone_number: phone_number
                })
            })    
            const response_data = await response.json();
            if (response_data.error) {
                display_toast('Error!', response_data.error, toast_background.ERROR);
            } else {
                display_toast('Success!', response_data.message, toast_background.SUCCESS);
            }
    } catch (err) {
        console.error('Fetch error:', err);
        display_toast('Error!', 'Something went wrong', toast_background.ERROR);
    }

}

