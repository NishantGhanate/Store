window.onload = function() {
  console.log('Page refreshed')
};


function buildProductList(){
  cardwrapper = document.getElementById('card-wrapper');
  // cardwrapper.innerHTML = '';
  var url = 'http://127.0.0.1:8000/api/product-list/';
  fetch(url)
  .then( (res) => res.json())
  .then( function(data){
    // console.log(data);
    for(d in data){
      // console.log(data[d].id);
      var img =  document.createElement("img");
      img.setAttribute('src','https://www.bigbasket.com/media/uploads/p/ml/10000431_15-bb-royal-pohaavalakkiavalchivda-thick.jpg');
      img.setAttribute('class','productImg');
      var button = document.createElement("button");
      button.setAttribute('class','');
      button.setAttribute('id','');
      button.innerHTML = 'Update';

      var node = document.createElement("div");
      node.setAttribute('class','card');
      node.appendChild(img);
      node.appendChild(button);
      document.getElementById("card-wrapper").appendChild(node);
    }
  });
}

function getToken(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}


// Product add  - form selection 
const productSelector = document.getElementById('product-selector');
const buttonClear = document.getElementById('button-clear');

const  product_id = document.getElementById('product_id');
const  input_name = document.getElementById('input_name');
const  input_brand = document.getElementById('input_brand');
const  input_manufacture = document.getElementById('input_manufacture');
const  input_subcategory= document.getElementById('input_subcategory');
const  input_productimage = document.getElementById('input_productimage');

if( buttonClear !=null ){
  buttonClear.addEventListener('click',clearForm);
  productSelector.addEventListener('click', getProductSelection);
}


function clearForm(e){
    product_id.value = '';
    input_name.value = '';
    input_brand.value = '';
    // input_manufacture.value = '';
    input_productimage.value =''
    input_subcategory.value = '';

    input_name.readOnly = false;
    input_brand.readOnly = false;
    input_subcategory.readOnly = false;
    input_productimage.readOnly = false;
}

function getProductSelection(e){
    console.log(e);
    var selected = productSelector.options[productSelector.selectedIndex];
    product_id.value = productSelector.value;
    input_name.value = selected.getAttribute('data-name');
    input_brand.value = selected.getAttribute('data-brand');
    // input_manufacture.value = selected.getAttribute('data-manufacture');
    input_subcategory.value = selected.getAttribute('data-subcategory');
    input_productimage.value = selected.getAttribute('data-productimage');

    input_name.readOnly = true;
    input_brand.readOnly = true;
    // input_manufacture.readOnly = true;
    input_subcategory.readOnly = true;
    input_productimage.readOnly = true;

}

// Product add 
const productAdded = document.querySelector('.product-added');
const addProductButton = document.querySelector('#button-add');
var input_weight = document.getElementById('input-weight');
var input_price = document.getElementById('input-price');
var input_quantity = document.getElementById('input-quantity');
if(addProductButton != null){
  addProductButton.addEventListener('click',createProductInfo);
  productAdded.addEventListener('click',subProductRemove);
}

function createProductInfo(e){
    e.preventDefault();
    if (input_weight.value  == ""){
      input_weight.classList.add('error');
      return
    }
    else if (input_weight.value  == ""){
      input_weight.classList.add('error');
      return
    }
    else if (input_quantity.value  == ""){
      input_quantity.classList.add('error');
      return
    }
    input_weight.classList.remove('error');
    input_weight.classList.remove('error');
    input_quantity.classList.remove('error');

    const divFormRow = document.createElement('div');
    divFormRow.classList.add('form-row');

    const inputValues = [input_weight,input_price,input_quantity];
    const names = ['weight[]','price[]','quantity[]'];

    for(var i = 0 ; i<names.length ; i++){
        const divCol = document.createElement('div');
        divCol.classList.add("col");
        const input = document.createElement('input');
        input.classList.add('form-control');
        input.readOnly = true;
        var inputName = document.createAttribute('name');
        inputName.value = names[i];
        var inpuValue = document.createAttribute('value');
        inpuValue.value = inputValues[i].value;
        inputValues[i].value = '';
        input.setAttributeNode(inputName);  
        input.setAttributeNode(inpuValue);  
        divCol.appendChild(input);
        divFormRow.appendChild(divCol); 
    }
    const div = document.createElement('div');
    const trashButton = document.createElement('button');
    trashButton.classList.add('form-control');
   

    trashButton.innerHTML = '<i class="fas fa-trash"> </i>';
    trashButton.classList.add('trash-btn');
    div.appendChild(trashButton);
    divFormRow.appendChild(div);
    productAdded.appendChild(divFormRow);

    
}

function subProductRemove(e){
    e.preventDefault();
    // console.log('Remove');
    // console.log(e.target);
    const item =  e.target;
    if(item.classList[1] === "trash-btn"){
        // console.log(e.path[2]);
        e.path[2].remove();
    }
}


// search list
function autocomplete(inp, searchableValues) {
  var currentFocus;
  inp.addEventListener('input',function(e){
      var searchList, macthes, i, val = this.value;
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      searchList = document.createElement("DIV");
      searchList.setAttribute("id", this.id + "autocomplete-list");
      searchList.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(searchList);
      for (i = 0; i < searchableValues.length; i++) {
          // can be improved
          if(searchableValues[i].substr(0, val.length).toUpperCase() == val.toUpperCase()){
              macthes = document.createElement("DIV");
              macthes.innerHTML = "<strong>" + searchableValues[i].substr(0, val.length) + "</strong>";
              macthes.innerHTML += searchableValues[i].substr(val.length);
              macthes.innerHTML += "<input type='hidden' value='" + searchableValues[i] + "'>";

              macthes.addEventListener("click", function(e) {
                  /*insert the value for the autocomplete text field:*/
                  inp.value = this.getElementsByTagName("input")[0].value;
                  closeAllLists();
              });
              searchList.appendChild(macthes);
          }
      }
  });

  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });

  function addActive(x) {
      /*a function to classify an item as "active":*/
      if (!x) return false;
      /*start by removing the "active" class on all items:*/
      removeActive(x);
      if (currentFocus >= x.length) currentFocus = 0;
      if (currentFocus < 0) currentFocus = (x.length - 1);
      /*add class "autocomplete-active":*/
      x[currentFocus].classList.add("autocomplete-active");
  }

  function removeActive(x) {
      /*a function to remove the "active" class from all autocomplete items:*/
      for (var i = 0; i < x.length; i++) {
        x[i].classList.remove("autocomplete-active");
      }
  }

  function closeAllLists(elmnt) {
      /*close all autocomplete lists in the document,
      except the one passed as an argument:*/
      var x = document.getElementsByClassName("autocomplete-items");
      for (var i = 0; i < x.length; i++) {
        if (elmnt != x[i] && elmnt != inp) {
          x[i].parentNode.removeChild(x[i]);
        }
      }
  }

  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

