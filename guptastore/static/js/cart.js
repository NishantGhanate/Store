// User side cart related functions

const productDiv = document.querySelector('.products');
if (productDiv != null){
    productDiv.addEventListener('click',addCartStore);
}


function addCartStore(e){
    e.preventDefault();
    const item =  e.target;
    // console.log(item);
    
    if(item.classList[0] === "update-cart"){
        var product_id = '';
        var action = '';
        console.log('Add to cart clicked');
        if(item.dataset.product_id != ""){
            product_id = item.dataset.product_id;
            action = item.dataset.action;  
            elem = e.path[5];
            if(user==='AnonymousUser'){
                console.log("User not logged in",user);
                addCookieItem(product_id,action);
                }
            else{
                uppdateUserOrder(product_id,action,null);
            }
        }
        
    }
    else if(item.classList[0]=="selected-product"){
        // console.log('Product selection changed');

        if(e.target.value != ""){
            var div = e.path[2];
            var buttons = div.getElementsByClassName("update-cart");
            for (var i = 0; i < buttons.length; i++){
                buttons[i].dataset.product_id = e.target.value;
            }
            var button = div.getElementsByClassName("edit-product");
            button[0].dataset.product_id = e.target.value;
        }
    }
    else if(item.classList[0]=="edit-product"){

        var product_id = item.dataset.product_id;
        console.log(product_id);
        if(product_id != ""){
            window.location.href = "/store/edit_product/"+product_id;
        }
        else {
            var div = e.path[2];
            var selected = div.getElementsByClassName("selected-product").value;
             
            alert("selected");
        }  
    }
}


const cartPage = document.querySelector('.cart-items'); 
if (cartPage != null){
    cartPage.addEventListener('click',updateCart);
    
}

function updateCart(e){
    e.preventDefault();
    const item =  e.target;
    var product_id = '';
    var action = '';
    var elem = '';
    if(item.classList[0] === "update-cart"){
        product_id = item.dataset.product_id;
        action = item.dataset.action;
        elem = e.path[3]; 
        if(user==='AnonymousUser'){
            console.log("User not logged in",user);
            // addCookieItem(product_id,action);
            }
        else{
            uppdateUserOrder(product_id,action,elem);
        } 
    }
    else if (item.classList[0] === "remove-button"){
        product_id = item.dataset.product_id;
        action = item.dataset.action; 
        elem = e.path[2];
        if(user==='AnonymousUser'){
            console.log("User not logged in",user);
            // addCookieItem(product_id,action);
            }
        else{
            uppdateUserOrder(product_id,action,elem);
        }
    }
}


function uppdateUserOrder(product_id,action,elem){

    const csrftoken = getToken('csrftoken');
    var url = '/update_item/'
    fetch(url ,{
        method :'POST',
        headers : {
            'Content-Type' : 'application/json',
            'X-CSRFToken'  : csrftoken
        },
        body: JSON.stringify({
            'product_id':product_id,
            'action' : action
        })
        
    })
    .then((response) => {
        return response.json()
    })
    .then((data) =>{
        navCountHtml = document.getElementById('navCount');
        cartCountHtml = document.getElementById('cartCount');
        if(data.item_quantity <= 0 && elem != null ){
            elem.remove();  
        }
        if(data.item_quantity < 100)
        {   
            if(elem != null){
                cartTotal = document.getElementById('cartTotal');
                item_quantity = elem.getElementsByClassName('item-quantity')[0];
                item_total = elem.getElementsByClassName('item-total')[0];

                item_quantity.innerHTML = data.item_quantity;
                item_total.innerHTML = data.item_total;
                cartTotal.innerHTML = data.order_total;
                cartCountHtml.innerHTML =  data.order_quantity;
            }
            navCountHtml.innerHTML = data.order_quantity;
        }
    });
}


function addCookieItem(product_id,action){
    console.log('Anon user adding itemt to cart');
    if(action=='add'){
        if(cart[product_id] == undefined){
            cart[product_id] = {'quantity': 1};
        }
        else{
            cart[product_id]['quantity'] += 1;
        }
    }
    else if(action=='remove'){
        cart[product_id]['quantity'] -= 1;
        if(cart[product_id]['quantity'] <= 0){
            console.log('Item removed from cart ');
            delete cart[product_id];
        }
    }
    console.log('Cart :' , cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=path=/'
}


function getCookie(name){
    var cookieArr = document.cookie.split(";");
    for(var i=0 ;  i < cookieArr.length; i++){
        var cookierPair = cookieArr[i].split("=");
        if(name == cookierPair[0].trim()){
            return decodeURIComponent(cookierPair[1]);
        }
    }
    return null;
}

var cart = JSON.parse(getCookie('cart'));
if(cart == null ){
    cart = {}
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=path=/'
}
console.log('cart cookie' , {...cart});