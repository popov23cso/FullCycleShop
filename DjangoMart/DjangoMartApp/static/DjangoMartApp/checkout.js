import { toast_background, display_toast, hide_element, show_element, send_api_request} from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#saveAddressBtn').addEventListener('click', save_address);

    const address_container = document.querySelector('#addressesContainer');
    address_container.addEventListener('click', (event) => {
    if (event.target.classList.contains('deleteAddressBtn')) {
        const btn = event.target;
        const parent = btn.closest('.card');
        const address_id = btn.dataset.id;
        remove_address(parent, address_id);
    }
    });
    
    const address_cards = document.querySelectorAll('.addressCard');
    address_cards.forEach(item => {
        item.addEventListener('click', e => {select_address(e.currentTarget)})
    })
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
    const response_data = await send_api_request('/add_address', request_body, 'POST')
    if (response_data.error) {
        display_toast('Error!', response_data.error, toast_background.ERROR);
    } else {
        display_toast('Success!', 'Added successfully', toast_background.SUCCESS);
        display_address(city, street, street_number, phone_number, response_data.id);
        address_count += 1;
        if (address_count >= 3) {
            let address_dropdown_selector = '#addressDropdown';
            hide_element(address_dropdown_selector);
        }
        address_container.dataset.addresscount = address_count;
    }
    address_dropdown.classList.remove('show');
    address_menu.classList.remove('show');
}

async function remove_address(parent_element, address_id) {
    const address_container = document.querySelector('#addressesContainer');
    let address_count = parseInt(address_container.dataset.addresscount);
    const request_body = {
                address_id: address_id
    }
    const response_data = await send_api_request('/remove_address', request_body, 'DELETE');
    if (response_data.error) {
        display_toast('Error!', response_data.error, toast_background.ERROR);
    } else {
        display_toast('Success!', 'Removed successfully', toast_background.SUCCESS);
        const related_body = parent_element.querySelector('.card-body');
        if (related_body.classList.contains('selectedAddress')) {
            disable_chekout();
        }
        parent_element.remove();
        address_count -= 1;
        let address_dropdown_selector = '#addressDropdown';
        show_element(address_dropdown_selector);
        address_container.dataset.addresscount = address_count;
    }
}

function display_address(city, street, street_number, phone_number, id) {
    const template = document.querySelector('#addressTemplate');
    const clone = template.content.cloneNode(true);
    const card = clone.querySelector('.addressCard');
    const city_el = clone.querySelector('#city');
    const street_el = clone.querySelector('#street');
    const street_num_el = clone.querySelector('#streetNum');
    const phone_num_el = clone.querySelector('#phoneNum');
    const delete_btn = clone.querySelector('.deleteAddressBtn');

    city_el.textContent = city;
    street_el.textContent = street;
    street_num_el.textContent = street_number;
    phone_num_el.textContent = phone_number;
    delete_btn.dataset.id = id;

    card.addEventListener('click',() => select_address(card));

    document.querySelector('#addressesContainer').appendChild(clone);
}


function select_address(address_box) {
    unselect_not_clicked_addresses();
    address_box.classList.remove('text-bg-warning');
    address_box.classList.add('text-bg-success');
    address_box.classList.add('selectedAddress');
    enable_checkout(address_box.dataset.id);
}

function enable_checkout(address_id) {
    const form_address_id = document.querySelector('#addressID');
    const checkout_btn = document.querySelector('#checkoutBtn');

    form_address_id.value = address_id;
    checkout_btn.style.display = 'block';
}

function disable_chekout() {
    const form_address_id = document.querySelector('#addressID');
    const checkout_btn = document.querySelector('#checkoutBtn');

    form_address_id.value = null;
    checkout_btn.style.display = 'none';
}

function unselect_not_clicked_addresses() {
    const address_cards = document.querySelectorAll('.addressCard');
    address_cards.forEach(item => {
        if (item.classList.contains('selectedAddress')) {
            item.classList.remove('selectedAddress');
            item.classList.remove('text-bg-success');
            item.classList.add('text-bg-warning');
        }
    })
}

