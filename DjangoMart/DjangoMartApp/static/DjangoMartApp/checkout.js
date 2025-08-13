import { getCSRFToken, toast_background, display_toast, hide_element, show_element} from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#saveAddressBtn').addEventListener('click', save_address);

    const container = document.querySelector('#addressesContainer');
    container.addEventListener('click', (event) => {
    if (event.target.classList.contains('deleteAddressBtn')) {
        const btn = event.target;
        const parent = btn.closest('.card');
        const { city, street, streetnum, phonenum } = btn.dataset;
        remove_address(parent, city, street, streetnum, phonenum);
    }
    });

})



async function save_address() {
    const city = document.querySelector('#dropdownCity').value;
    const street = document.querySelector('#dropdownStreet').value;
    const street_number = document.querySelector('#dropdownStreetNumber').value;
    const phone_number = document.querySelector('#dropdownPhoneNumber').value;
    const address_dropdown = document.querySelector('#addressDropdown');
    const address_menu = document.querySelector('#addressMenu');
    const address_container = document.querySelector('#addressesContainer');
    let address_count = parseInt(address_container.dataset.addresscount);
    const request_body = {
                city: city,
                street: street,
                street_number: street_number,
                phone_number: phone_number
    }
    const response_data = send_api_request('/add_address', request_body)
            if (response_data.error) {
                display_toast('Error!', response_data.error, toast_background.ERROR);
            } else {
                display_toast('Success!', 'Added successfully', toast_background.SUCCESS);
                display_address(city, street, street_number, phone_number);
                address_count += 1;
                if (address_count >= 3) {
                    let address_dropdown_selector = '#addressDropdown';
                    hide_element(address_dropdown_selector);
                }
                address_container.dataset.addresscount = address_count;
            }
    } catch (err) {
        console.error('Fetch error:', err);
        display_toast('Error!', 'Something went wrong', toast_background.ERROR);
    }
    address_dropdown.classList.remove('show');
    address_menu.classList.remove('show');
}

async function remove_address(parent_element, city, street, street_number, phone_number) {
    const address_container = document.querySelector('#addressesContainer');
    let address_count = parseInt(address_container.dataset.addresscount);
    const request_body = {
                city: city,
                street: street,
                street_number: street_number,
                phone_number: phone_number
    }
    const response_data = send_api_request('/remove_address', request_body)
            if (response_data.error) {
                display_toast('Error!', response_data.error, toast_background.ERROR);
            } else {
                display_toast('Success!', 'Removed successfully', toast_background.SUCCESS);
                parent_element.remove();
                address_count -= 1;
                let address_dropdown_selector = '#addressDropdown';
                show_element(address_dropdown_selector);
                address_container.dataset.addresscount = address_count;

            }
    } catch (err) {
        console.error('Fetch error:', err);
        display_toast('Error!', 'Something went wrong', toast_background.ERROR);
    }
}

function display_address(city, street, street_number, phone_number) {
    const template = document.querySelector('#addressTemplate');
    const clone = template.content.cloneNode(true);
    const city_el = clone.querySelector('#city');
    const street_el = clone.querySelector('#street');
    const street_num_el = clone.querySelector('#streetNum');
    const phone_num_el = clone.querySelector('#phoneNum');
    const delete_btn = clone.querySelector('.deleteAddressBtn');

    city_el.textContent = city;
    street_el.textContent = street;
    street_num_el.textContent = street_number;
    phone_num_el.textContent = phone_number;
    delete_btn.dataset.city = city;
    delete_btn.dataset.street = street;
    delete_btn.dataset.streetnum = street_number;
    delete_btn.dataset.phonenum = phone_number;

    document.querySelector('#addressesContainer').appendChild(clone);
}
