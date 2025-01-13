// Добавяне на нова тема
document.getElementById("addTopicForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const titleInput = document.getElementById("title");
    const title = titleInput.value.trim();

    if (!title) {
        alert("Topic title is required.");
        return;
    }

    fetch("/api/add-topic", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: title }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Topic added successfully!");
                location.href = `/forum/topic/${data.topic.id}`; // Пренасочва към новата тема
            } else {
                alert(data.error || "An error occurred while creating the topic.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An unexpected error occurred. Please try again.");
        });
});

// Добавяне на пост в тема
document.getElementById("addPostForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const nameInput = document.getElementById("name");
    const messageInput = document.getElementById("message");
    const name = nameInput.value.trim() || "Anonymous";
    const message = messageInput.value.trim();

    if (!message) {
        alert("Message is required.");
        return;
    }

    const topicId = window.location.pathname.split("/").pop();

    fetch(`/api/add-post/${topicId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name, message: message }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                const postsList = document.getElementById("posts").querySelector("ul");
                const newPost = document.createElement("li");
                newPost.innerHTML = `
                    <strong>${data.post.name}:</strong> ${data.post.message}
                    <button class="delete-post" data-post-id="${data.post.id}">Delete</button>
                `;
                postsList.appendChild(newPost);

                // Добавяне на слушател за изтриване на новия пост
                newPost.querySelector(".delete-post").addEventListener("click", deletePost);

                // Изчистване на формата
                nameInput.value = "";
                messageInput.value = "";
            } else {
                alert(data.error || "An error occurred.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An unexpected error occurred.");
        });
});

// Изтриване на пост
function deletePost(event) {
    const button = event.target;
    const postId = button.getAttribute("data-post-id");
    const topicId = window.location.pathname.split("/").pop();

    if (!confirm("Are you sure you want to delete this post?")) return;

    fetch(`/api/delete-post/${topicId}/${postId}`, {
        method: "DELETE",
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                button.parentElement.remove(); // Премахва публикацията от списъка
            } else {
                alert(data.error || "An error occurred while deleting the post.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An unexpected error occurred.");
        });
}

// Добавяне на слушатели за изтриване на всички съществуващи постове
document.querySelectorAll(".delete-post").forEach((button) => {
    button.addEventListener("click", deletePost);
});
document.getElementById("addCommentForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim() || "Anonymous";
    const comment = document.getElementById("comment").value.trim();
    const topicId = window.location.pathname.split("/").pop();

    if (!comment) {
        alert("Comment is required.");
        return;
    }

    fetch(`/api/add-comment/${topicId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name, comment: comment }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            const commentsList = document.getElementById("comments-list");
            const newComment = document.createElement("li");
            newComment.innerHTML = `<strong>${data.comment.author}:</strong> ${data.comment.text}`;
            commentsList.appendChild(newComment);

            // Изчистване на формата
            document.getElementById("name").value = "";
            document.getElementById("comment").value = "";
        } else {
            alert(data.error || "An error occurred.");
        }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("An unexpected error occurred.");
    });
});
document.getElementById("addTopicForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const title = document.getElementById("title").value.trim();
    const sectionId = window.location.pathname.split("/").pop();
    fetch(`/forum/section/${sectionId}/add-topic`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: title }),
    }).then(response => response.json()).then(data => location.reload());
});
document.getElementById("addPostForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const author = document.getElementById("author").value.trim() || "Anonymous";
    const message = document.getElementById("message").value.trim();
    const topicId = window.location.pathname.split("/").pop();
    fetch(`/forum/topic/${topicId}/add-post`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ author: author, message: message }),
    }).then(response => response.json()).then(data => location.reload());
});


