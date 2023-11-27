let cart = [];
const addToCartLinks = document.querySelectorAll('.func-addToCart');
addToCartLinks.forEach(element => {
    element.addEventListener('click', toggleCartItems)
});

const viewCartBtn = document.querySelector('#view-cart-btn')
viewCartBtn.addEventListener('click', populateCart)

function populateCart(){
    cart = [];    
    // populate cart
    for(let i =0; i < addToCartLinks.length; i++){
        let element = addToCartLinks[i]
        if(element.dataset.inCart == 'false') continue;
        let [_, assetId, orgId] = element.id.split('_')
        cart.push({
            'assetId':assetId,
            'orgId': orgId,
            'assetName': element.dataset.assetName,
            'orgName': element.dataset.orgName,
            'price': element.dataset.price,
            'qty': 0
        })
    }

    // create table out of the cart
    let cartShow = document.querySelector('#cartShow')
    let cartTable;
    cartTable = `
    <table class="table table-bordered">
        <thead>
            <tr>
                <th style="width: 25%;">Asset Name</th>
                <th style="width: 30%;">Supplier</th>
                <th style="width: 15%;">Unit Price</th>
                <th style="width: 15%;">Quantity</th>
                <th style="width: 15%;">Total</th>
            </tr>
        </thead>
    `;
    for(let i = 0; i < cart.length; i++){
        cartTable += `
            <tr>
                <td>${cart[i].assetName}</td>
                <td>${cart[i].orgName}</td>
                <td>${cart[i].price}</td>
                <td>
                    <input type="number" class="form-control" onchange="updatePrice(this.value, ${cart[i].price}, '#price_${cart[i].assetId}_${cart[i].orgId}')"/>
                </td>
                <td>
                    <p id="price_${cart[i].assetId}_${cart[i].orgId}"></p>
                </td>
            </tr>
            `;
    }
    cartTable += `
            <tr>
                <th colspan="4"> Grand Total </th>
                <td> <p id="total_price">0</p> </td> 
            </tr>
    </table>
    `;
    cartShow.innerHTML = cartTable

    
}

function updatePrice(qty, val, selector){
    document.querySelector(selector).innerHTML = val * qty;
    [_, assetId, orgId] = selector.split('_')
    for(let i = 0; i < cart.length; i++){
        if(cart[i].assetId == assetId && cart[i].orgId == orgId){
            cart[i].qty = qty
        }
    }

    let cartItemPriceElements = document.querySelectorAll('[id^=price_]');
    let total_price = 0
    for(let i = 0; i < cartItemPriceElements.length; i++){
        cartItemPriceElementText = cartItemPriceElements[i].innerText;
        if (Number(cartItemPriceElementText) != NaN){
            total_price += Number(cartItemPriceElementText);
        } 
        
    }

    document.querySelector('#total_price').innerHTML = total_price;
}
function toggleCartItems(event){
    event.stopPropagation();
    let addToCartLink = event.target;
    
    if(addToCartLink.dataset.inCart == 'false'){
        addToCartLink.classList.remove('btn-primary')
        addToCartLink.classList.add('btn-outline-primary')
        addToCartLink.dataset.inCart = 'true'
        addToCartLink.innerHTML = 'Remove from Cart'
    }else{
        addToCartLink.classList.remove('btn-outline-primary')
        addToCartLink.classList.add('btn-primary')
        addToCartLink.dataset.inCart = 'false'
        addToCartLink.innerHTML = 'Add to Cart'
    }
}

document.querySelector('#submitCheckoutBtn').addEventListener('click', checkout);
function checkout(){
    document.querySelector('#cartText').value = encodeURI(JSON.stringify({cart: cart})); 
    document.querySelector('#checkoutForm').querySelector('#submit').click()  
}