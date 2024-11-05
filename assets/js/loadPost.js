async function loadPost() {
    const postId = new URLSearchParams(window.location.search).get('id');
    
    const response = await fetch('posts/posts.json'); // Certifique-se do caminho
    const posts = await response.json();

    const post = posts.find(p => p.id == postId);
    const postIndex = posts.findIndex(p => p.id == postId);

    if (post) {
        document.getElementById('post-title').textContent = post.title;
        document.getElementById('post-date').textContent = post.date;
        document.getElementById('post-image').src = post.image;
        document.getElementById('post-image').alt = post.title;

        const postContent = document.getElementById('post-content');
        post.content.forEach(section => {
            const heading = document.createElement('h2');
            heading.className = 'sub-heading';
            heading.textContent = section.heading;

            const text = document.createElement('p');
            text.className = 'post-text';
            text.innerHTML = section.text;

            postContent.appendChild(heading);
            postContent.appendChild(text);
        });

        const prevPost = posts[postIndex - 1];
        const nextPost = posts[postIndex + 1];

        if (prevPost) {
            document.getElementById('prev-post').href = `post.html?id=${prevPost.id}`;
            document.getElementById('prev-post').textContent = prevPost.title;
        } else {
            document.getElementById('prev-post').style.display = 'none';
        }

        if (nextPost) {
            document.getElementById('next-post').href = `post.html?id=${nextPost.id}`;
            document.getElementById('next-post').textContent = nextPost.title;
        } else {
            document.getElementById('next-post').style.display = 'none';
        }
    }
}

loadPost();
