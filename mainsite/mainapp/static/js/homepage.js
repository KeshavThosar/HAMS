let validateAssetBtn = document.querySelector('#validateAssetId')
validateAssetBtn.addEventListener('click', async event => {
    event.stopPropagation()
    let inputAssetId = document.querySelector('#inputAssetId')
    let inputQty = document.querySelector('#inputQty')
    let inputPrice = document.querySelector('#inputPrice')
    let hiddenAssetId = document.querySelector('#assetId')
    let assetId = inputAssetId.value;
    let assetName = await fetchAssetName(assetId)

    if (assetName != 'N/A') {
        hiddenAssetId.value = assetId
        inputAssetId.value = assetName
        inputAssetId.disabled = true
        validateAssetBtn.innerHTML = 'Reset'
        let asset = document.querySelector('#asset_'+assetId);

        if(asset && inputQty) inputQty.value = asset.dataset.qtyAvailable;
        if(asset && inputPrice) inputPrice.value = asset.dataset.pricePerUnit;
        
    }else{
        inputAssetId.value = ''
        inputAssetId.disabled = false
        hiddenAssetId.value = ''
        validateAssetBtn.innerHTML = 'Validate'
    }
    
})

async function fetchAssetName(assetId){
    res = await fetch('/app/api/getAssetName?asset_id='+assetId);
    text = await res.text()
    return text
}


document.querySelector('#submitAddAssetFormBtn').addEventListener('click', submitAddAssetForm)
function submitAddAssetForm(){
    addAssetForm = document.querySelector('#addAssetForm')
    addAssetForm.querySelector('#submit').click()
}