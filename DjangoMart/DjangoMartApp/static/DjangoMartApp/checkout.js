import { getCSRFToken, toast_background, display_toast} from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('saveAddressBtn').addEventListener('click', save_address);

  document.querySelectorAll('.deleteAddressBtn').forEach(button => {
    button.addEventListener('click', e => {
        const btn = e.currentTarget;
        const parent = btn.closest('.card');
        const { city, street, streetnum, phonenum } = btn.dataset;
            remove_address(parent, city, street, streetnum, phonenum);
        });
    });
})



async function save_address() {
    const city = document.getElementById('dropdownCity').value;
    const street = document.getElementById('dropdownStreet').value;
    const street_number = document.getElementById('dropdownStreetNumber').value;
    const phone_number = document.getElementById('dropdownPhoneNumber').value;
    const address_dropdown = document.getElementById('addressDropdown');
    const address_menu = document.getElementById('addressMenu');

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
                display_toast('Success!', 'Added successfully', toast_background.SUCCESS);
                display_address(city, street, street_number, phone_number);
            }
    } catch (err) {
        console.error('Fetch error:', err);
        display_toast('Error!', 'Something went wrong', toast_background.ERROR);
    }
    address_dropdown.classList.remove('show');
    address_menu.classList.remove('show');
}

async function remove_address(parent_element, city, street, street_number, phone_number) {
    try {
        const response = await fetch ('/remove_address', {
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
                display_toast('Success!', 'Removed successfully', toast_background.SUCCESS);
                parent_element.remove();
            }
    } catch (err) {
        console.error('Fetch error:', err);
        display_toast('Error!', 'Something went wrong', toast_background.ERROR);
    }
}

function display_address(city, street, street_number, phone_number) {
    const template = document.getElementById('addressTemplate');
    const clone = template.content.cloneNode(true);
    const city_el = clone.getElementById('city');
    const street_el = clone.getElementById('street');
    const street_num_el = clone.getElementById('streetNum');
    const phone_num_el = clone.getElementById('phoneNum');
    city_el.textContent = city;
    street_el.textContent = street;
    street_num_el.textContent = street_number;
    phone_num_el.textContent = phone_number;

    document.getElementById('addressesContainer').appendChild(clone);
}
