const ratingButtons = document.querySelectorAll('.rating-buttons');

ratingButtons.forEach(button => {
    button.addEventListener('click', event => {
        // Getting the rating value from the data attribute of the button
        const value = parseInt(event.target.dataset.value)
        const postId = parseInt(event.target.dataset.post)
        const ratingSum = button.querySelector('.rating-sum');
        // Create a FormData object to send data to the server
        const formData = new FormData();
        // Add article id, button value
        formData.append('post_id', postId);
        formData.append('value', value);
        // Sending an AJAX Request to the server
        fetch("/rating/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "X-Requested-With": "XMLHttpRequest",
            },
            body: formData
        }).then(response => response.json())
        .then(data => {
            // Update the value on the button
            ratingSum.textContent = data.rating_sum;
        })
        .catch(error => console.error(error));
    });
});