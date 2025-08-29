document.addEventListener("DOMContentLoaded", function () {
    // Refresh streams every 5 seconds
    setInterval(fetchUpdates, 5000);

    // Attach event listener for comment submissions
    document.body.addEventListener("submit", function (event) {
        if (event.target.classList.contains("comment-form")) {
            event.preventDefault();
            submitComment(event.target);
        }
    });
});

// Fetch global or follower stream updates
function fetchUpdates() {
    const url = window.location.pathname.includes("follower_stream")
        ? "/socialnetwork/get-follower"
        : "/socialnetwork/get-global";

    fetch(url)
        .then(response => response.json())
        .then(data => updatePosts(data))
        .catch(error => console.error("Error fetching posts:", error));
}

// Update posts on the page
function updatePosts(data) {
    const postContainer = document.getElementById("post-list");

    data.posts.forEach(post => {
        if (!document.getElementById(`id_post_div_${post.id}`)) {
            // Create new post element if it doesn't exist
            const postElement = document.createElement("div");
            postElement.id = `id_post_div_${post.id}`;
            postElement.classList.add("post-container");
            postElement.innerHTML = `
                <p>
                    <a href="/profile/${post.user_id}/" id="id_post_profile_${post.id}">
                        ${post.user_fullname}
                    </a>
                    - <span id="id_post_text_${post.id}">${post.text}</span>
                    - <span id="id_post_date_time_${post.id}">${formatTimestamp(post.creation_time)}</span>
                </p>
                <div id="comments_${post.id}" class="comments-section"></div>
                <form class="comment-form" data-post-id="${post.id}">
                    <input type="text" id="id_comment_input_text_${post.id}" name="comment_text" placeholder="Add a comment..." required>
                    <button type="submit" id="id_comment_button_${post.id}">Comment</button>
                </form> 
            `;
            postContainer.prepend(postElement);
        }
        updateComments(post.id, post.comments);
    });
}

// Update comments for a specific post
function updateComments(postId, comments) {
    const commentSection = document.getElementById(`comments_${postId}`);

    comments.forEach(comment => {
        if (!document.getElementById(`id_comment_div_${comment.id}`)) {
            const commentElement = document.createElement("div");
            commentElement.id = `id_comment_div_${comment.id}`;
            commentElement.classList.add("comment-container");
            commentElement.innerHTML = `
                <p>
                    <a href="/profile/${comment.user_id}/" id="id_comment_profile_${comment.id}">
                        ${comment.user_fullname}
                    </a>
                    - <span id="id_comment_text_${comment.id}">${comment.text}</span>
                    - <span id="id_comment_date_time_${comment.id}">${formatTimestamp(comment.creation_time)}</span>
                </p>
            `;
            commentSection.appendChild(commentElement);
        }
    });
}

// Submit comment via AJAX
function submitComment(form) {
    const postId = form.dataset.postId;
    const formData = new FormData(form);
    formData.append("post_id", postId);

    fetch("/socialnetwork/add-comment", {
        method: "POST",
        body: formData,
        headers: {
            "X-CSRFToken": getCSRFToken(), // Ensure CSRF token is sent
        },
        credentials: "same-origin", // REQUIRED for CSRF authentication
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        if (data.success) {
            updateComments(postId, [data.comment]);
            form.reset();
        } else {
            console.error("Error submitting comment:", data.error);
        }
    })
    .catch(error => console.error("Fetch error:", error));
}


function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    const month = date.getMonth() + 1; // getMonth returns 0-11
    const day = date.getDate();
    const year = date.getFullYear();

    let hours = date.getHours();
    const minutes = date.getMinutes();
    const ampm = hours >= 12 ? "PM" : "AM";
    hours = hours % 12;
    if (hours === 0) hours = 12;
    // Pad minutes to always have 2 digits:
    const minuteStr = minutes < 10 ? "0" + minutes : minutes;
    return `${month}/${day}/${year} ${hours}:${minuteStr} ${ampm}`;
}




// Retrieve CSRF token from hidden input
function getCSRFToken() {
    return document.getElementById("csrf_token")?.value || "";
}

