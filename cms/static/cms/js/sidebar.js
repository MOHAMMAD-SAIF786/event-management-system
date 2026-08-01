const sidebar=document.querySelector(".sidebar");
const menuBtn=document.getElementById("menuBtn");

menuBtn.addEventListener("click",()=>{

    if(window.innerWidth<=768){

        sidebar.classList.toggle("active");

    }else{

        sidebar.classList.toggle("collapsed");

    }

});