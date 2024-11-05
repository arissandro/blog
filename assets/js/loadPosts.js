async function loadPosts() {
    try {
        const response = await fetch('posts/posts.json'); // Certifique-se do caminho
        const posts = await response.json();
        const postsContainer = document.getElementById('posts-container');

        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post-preview';
            postElement.innerHTML = `
                <h2><a href="post.html?id=${post.id}">${post.title}</a></h2>
                <p><em>${post.date}</em></p>
                <img src="${post.image}" alt="${post.title}" />
                <p>${post.content[0].text.slice(0, 100)}...</p>
            `;
            postsContainer.appendChild(postElement);
        });
    } catch (error) {
        console.error('Erro ao carregar posts:', error);
    }
}

// Carregar os posts quando a página for aberta
loadPosts();
