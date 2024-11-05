//filter js
$(document).ready(function(){

    //separa os poste por filtro
    $(".filter-item").click(function(){
        const value = $(this).attr('data-filter');

        if(value == 'tudo'){
            $(".post-box").show("1000");
        }
        else{
            $(".post-box").not("." + value).hide("1000");
            $(".post-box").filter("." + value).show("1000");
        }
    });
    //adiciona efeito "active" aos filtros de forma individual
    $(".filter-item").click(function(){
        $(this).addClass("active-filter").siblings().removeClass("active-filter");
    });
});

// background do cabeçalho muda quando scrollado
let header = document.querySelector("header")

window.addEventListener("scroll", () => {
    header.classList.toggle("shadow", window.scrollY > 0);
});