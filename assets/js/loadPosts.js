async function loadPosts() {
    try {
        const response = await fetch('posts/posts.json'); // Este caminho deve estar correto
        const posts = await response.json();
        const postsContainer = document.getElementById('posts-container');

        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post-preview';
            postElement.innerHTML = `
                <h2><a href="/blog/post-page.html?id=${post.id}">${post.title}</a></h2> <!-- Incluindo o nome do repositório -->
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
