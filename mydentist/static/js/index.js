

let header=document.querySelector(".my-header")
let navSpace=document.querySelector(".nav-space")


navSpace.querySelector("button").addEventListener("click", ()=>{
    document.querySelector(".my-header").classList.add("show")
})
header.querySelector("#close_btn").addEventListener("click", ()=>{
    document.querySelector(".my-header").classList.remove("show")
})