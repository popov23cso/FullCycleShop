import { toast_background, display_toast, send_api_request} from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', e => {update_stars(e.currentTarget, stars)})
    })

    const save_review_btns = document.querySelectorAll('#saveReviewBtn');
    save_review_btns.forEach(btn => {
        btn.addEventListener('click', e => {save_review(e.currentTarget)})
    })

    const delete_review_btns = document.querySelectorAll('#deleteReviewBtn');
    delete_review_btns.forEach(btn => {
        btn.addEventListener('click', e => {delete_review(e.currentTarget)})
    })
})



function update_stars(target_star, all_stars) {
    const rating = target_star.dataset.value;
    all_stars.forEach(s => {
        const is_active = s.dataset.value <= rating;
        s.classList.toggle('bi-star-fill', is_active);
        s.classList.toggle('text-warning', is_active);
        s.classList.toggle('bi-star', !is_active);
    });
}

async function save_review(save_button) {
    const purchase_item_id = save_button.dataset.itemid;
    const star_group_id = `starGroup${purchase_item_id}`;
    const rating = get_review_star_count(star_group_id);

    if (rating <= 0) {
        let error_mesage = 'Please select star rating'
        display_toast('Error!', error_mesage, toast_background.ERROR);
    }

    const comment_id = `#comment${purchase_item_id}`;
    const comment = document.querySelector(comment_id).value;

    const request_body = {
        purchase_item_id: purchase_item_id,
        rating: rating,
        comment: comment
    }

    const response_data = await send_api_request('/manage_review', request_body, 'POST');
    
    if (response_data.error) {
        display_toast('Error!', response_data.error, toast_background.ERROR);
    } else {
        location.reload();
    }
}

function get_review_star_count(star_group_id) {
    const stars = document.querySelectorAll(`#${star_group_id}`);
    let star_count = 0;

    stars.forEach(star => {
        if ( star.classList.contains('bi-star-fill') ) {
            star_count += 1;
        }
    })

    return star_count
}

async function delete_review(delete_button) {
    const review_id = delete_button.dataset.reviewid;

    const request_body = {
        review_id: review_id
    }

    const response_data = await send_api_request('/delete_review', request_body, 'DELETE');
    
    if (response_data.error) {
        display_toast('Error!', response_data.error, toast_background.ERROR);
    } else {
        location.reload();
    }
}