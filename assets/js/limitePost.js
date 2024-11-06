document.addEventListener("DOMContentLoaded", function() {
    // Seleciona todos os elementos com a classe home-post-container
    var posts = document.querySelectorAll('.home-post-container');
    
    posts.forEach(function(post) {
      var content = post.querySelector('.home-post-content');
      var link = post.querySelector('.home-post-link');
      
      // Verifica o tamanho do conteúdo e sempre mantém o link "Leia mais..."
      if (content.scrollHeight > content.clientHeight) {
        link.style.display = 'inline'; // Garante que o link "Leia mais..." sempre seja exibido
      }
    });
  });