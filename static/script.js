const dropArea = document.querySelector(".drag-area"),
dragText = dropArea.querySelector("header"),
button = dropArea.querySelector("button"),
input = dropArea.querySelector("input");
let file; //this is a global variable and we'll use it inside multiple functions
const baseURL = "http://127.0.0.1:5000";
const uploadURL = `${baseURL}/filenew`;
button.onclick = ()=>{
  input.click(); //if user click on the button then the input also clicked
}
 
input.addEventListener("change", function(){
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = this.files[0];
  dropArea.classList.add("active");
  showFile(); //calling function
});
 
 
//If user Drag File Over DropArea
dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});
 
//If user leave dragged File from DropArea
dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
});
 
//If user drop File on DropArea
dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); //preventing from default behaviour
  //getting user select file and [0] this means if user select multiple files then we'll select only the first one
  file = event.dataTransfer.files[0];
  showFile(); //calling function
});
 
function showFile(){
    // let fileReader = new FileReader(); //creating new FileReader object
    const newuploaded = document.querySelector(".upnow")
    console.log(file.name)
    newuploaded.innerHTML = file.name;
    const xhr = new XMLHttpRequest();
    const formData = new FormData();
    formData.append("myfile", file);
    var c = document.getElementById("mybut")
    c.addEventListener("click",function(){
        console.log("Enetr");
        xhr.open("POST", uploadURL);
        xhr.send(formData);
    });
    
  
  
}