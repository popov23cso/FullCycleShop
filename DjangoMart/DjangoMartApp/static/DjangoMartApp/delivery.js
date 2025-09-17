import { toast_background, display_toast, send_api_request} from './functions.js';

document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', e => {update_stars(e.currentTarget, stars)})
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