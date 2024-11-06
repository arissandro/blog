async function loadPosts() {
    try {
        const response = await fetch('../postes/postes.json'); // Carregar JSON dos posts
        if (!response.ok) {
            throw new Error('Erro ao carregar os posts.');
        }
        
        const posts = await response.json(); // Converter JSON para objeto
        const postsContainer = document.getElementById('posts-container');

        // Limpar o contêiner de posts antes de inserir novos dados
        postsContainer.innerHTML = '';

        // Inserir cada post na página
        posts.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'post-preview';

            postElement.innerHTML = `
                <h2><a href="${post.link}">${post.title}</a></h2>
                <p><em>${post.date}</em></p>
                <img src="${post.image}" alt="${post.title}" />
                <p>${post.content[0].text.slice(0, 100)}...</p>
            `;

            postsContainer.appendChild(postElement);
        });
    } catch (error) {
        console.error('Erro ao carregar os posts:', error);
    }
}

// Carregar os posts ao iniciar a página
document.addEventListener('DOMContentLoaded', loadPosts);
