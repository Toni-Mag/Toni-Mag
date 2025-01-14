//// Добавяне на тема
document.getElementById("addTopicForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const title = document.getElementById("title").value.trim();
    const author = document.getElementById("author").value.trim() || "Anonymous";

    if (!title) {
        alert("Topic title is required.");
        return;
    }

    fetch("/api/add-topic", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title: title, author: author }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to create topic.");
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                location.href = `/forum/topic/${data.topic.id}`;
            } else {
                alert(data.error || "An error occurred while creating the topic.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An unexpected error occurred.");
        });
});

// Добавяне на пост
document.getElementById("addPostForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim() || "Anonymous";
    const message = document.getElementById("message").value.trim();
    const topicId = window.location.pathname.split("/").pop();

    if (!message) {
        alert("Message is required.");
        return;
    }

    fetch(`/api/add-post/${topicId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: name, message: message }),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to submit the post.");
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                const postsList = document.getElementById("posts").querySelector("ul");
                const newPost = document.createElement("li");
                newPost.innerHTML = `
                    <strong>${data.post.name}:</strong> ${data.post.message}
                    <button class="delete-post" data-post-id="${data.post.id}">Delete</button>
                `;
                postsList.appendChild(newPost);

                // Изчистване на формата
                document.getElementById("name").value = "";
                document.getElementById("message").value = "";
            } else {
                alert(data.error || "An error occurred.");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An unexpected error occurred.");
        });
});

// Добавяне на коментар
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
            "Content-Type": "application/json", // Задължително заглавие
        },
        body: JSON.stringify({
            name: document.getElementById("name").value.trim() || "Anonymous",
            comment: document.getElementById("comment").value.trim(),
        }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            // Добавяне на коментара в DOM
            const commentsList = document.getElementById("comments-list");
            const newComment = document.createElement("li");
            newComment.innerHTML = `<strong>${data.comment.author}:</strong> ${data.comment.text}`;
            commentsList.appendChild(newComment);
    
            // Изчистване на полетата
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
    
// Изтриване на публикация
document.querySelectorAll(".delete-post").forEach((button) => {
    button.addEventListener("click", function (event) {
        const topicId = window.location.pathname.split("/").pop();
        const postId = button.getAttribute("data-post-id");

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
    });
});
