// 驗證登入狀態
authenticateUser();

// 取得訂單資訊
(function showOrderId(){
    const urlParams = new URLSearchParams(window.location.search)
    const order_id = urlParams.get('number');
    let orderIdElem = document.querySelector('#order_id');
    orderIdElem.textContent = order_id
})();