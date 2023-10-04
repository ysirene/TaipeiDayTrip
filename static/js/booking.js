let bookingData = {};

// 驗證會員身分後取得景點資訊
(function authenticateUser(){
    if(localStorage.getItem('token')){
        let token = localStorage.getItem('token');
        let src = '/api/user/auth';
        let options = {
            method: 'GET',
            headers:{
                'authorization': `Bearer ${token}`
            }
        };
        ajax(src, options).then((data) => {
            if(data['data'] != null){
                signinStatus = true;
                let bodyElem = document.getElementsByTagName('body')[0];
                let memberNameElem = document.querySelectorAll('#member_name');
                let memberEmailElem = document.querySelector('#member_email');
                memberNameElem[0].textContent = data['data']['name'];
                memberNameElem[1].value = data['data']['name'];
                memberEmailElem.value = data['data']['email'];
                bodyElem.style.display = 'block';
                getBookingInfo();
            }else{
                window.location.href = '/'; 
            };
        }).catch((error) => {
            console.log(error);
        });
    }else{
        window.location.href = '/';
    };
})();

// 取得預定行程資訊
function getBookingInfo(){
    let token = localStorage.getItem('token');
    let src = '/api/booking';
    let options = {
        method: 'GET',
        headers:{
            'authorization': `Bearer ${token}`
        }
    };
    ajax(src, options).then((data) => {
        if(data['data'] != null){
            let bookingInfoElem = document.querySelector('#booking_info');
            let attractionNameElem = document.querySelector('#attraction_name');
            let attractionAddressElem = document.querySelector('#attraction_address');
            let attractionImgElem =  document.querySelector('#attraction_img');
            let bookingDateElem = document.querySelector('#booking_date');
            let bookingTimeElem = document.querySelector('#booking_time');
            let bookingPriceElem = document.querySelector('#booking_price');
            let amountElem = document.querySelector('#amount');
            let bookingDate = new Date(data['data']['date']);
            let year = bookingDate.getFullYear();
            let month = (bookingDate.getMonth() + 1).toString().padStart(2, '0');
            let day = bookingDate.getDate().toString().padStart(2, '0');
            let formattedDate = `${year}-${month}-${day}`;
            let bookingTime = data['data']['time'] == 'forenoon'? '早上9點到中午12點': '下午1點到4點';
            bookingInfoElem.className= '' ;
            attractionNameElem.textContent = data['data']['attraction']['name'];
            attractionAddressElem.textContent = data['data']['attraction']['address'];
            attractionImgElem.setAttribute('src', data['data']['attraction']['image']);
            bookingDateElem.textContent = formattedDate;
            bookingTimeElem.textContent = bookingTime;
            bookingPriceElem.textContent = data['data']['price'];
            amountElem.textContent = data['data']['price'];
            bookingData = {
                'price': data['data']['price'],
                'trip': {
                    'attraction': data['data']['attraction'],
                    'date': formattedDate,
                    'time': data['data']['time']
                }
            };
        }else{
            let bookingInfoElem = document.querySelector('#booking_info--none');
            bookingInfoElem.className= '' ;
        };
    }).catch((error) => {
        console.log(error);
    });

};

// 顯示登出按鈕
(function changeToSignOutBtn(){
    let memberBtnElem = document.querySelector('#member_btn');
    memberBtnElem.textContent = '登出系統';
    memberBtnElem.setAttribute('onclick', 'signout()');
    memberBtnElem.classList.remove('elem--invisible');
})();

// 點擊icon刪除預定行程
function delBookingItem(){
    let token = localStorage.getItem('token');
    let src = '/api/booking';
    let options = {
        method: 'DELETE',
        headers:{
            'authorization': `Bearer ${token}`
        }
    };
    ajax(src, options);
    location.reload();
};

// 建立TayPay表單
(function createCreditCardFrom(){
    TPDirect.setupSDK(137082, 'app_Nv7lGU2I3ImfvkXyR3ogZN50pFRpu6ALDbvas5xbRly0foZJMB9KCiUWNI1o', 'sandbox');
    let fields = {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****',
            style:{
                'border-radius': '5px'
            }
        },
        expirationDate: {
            element: '#card-expiration-date',
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'CCV'
        }
    };
    TPDirect.card.setup({
        fields: fields,
        styles: {
            // Style all elements
            'input': {
                'font-size': '16px',
                'font-weight': '500',
                'font-family':'"Noto Sans TC", sans-serif'
            },
            // style focus state
            ':focus': {
                'color': 'black'
            },
            // style valid state
            '.valid': {
                'color': 'green'
            },
            // style invalid state
            '.invalid': {
                'color': 'red'
            }
        },
        // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
        isMaskCreditCardNumber: true,
        maskCreditCardNumberRange: {
            beginIndex: 6,
            endIndex: 11
        }
    });
})();

// 檢查信用卡資訊是否填寫正確
TPDirect.card.onUpdate(function (update) {
    let submitBtn = document.querySelector('.form__submit');
    if (update.canGetPrime) {
        // Enable submit Button to get prime.
        submitBtn.removeAttribute('disabled');
    } else {
        submitBtn.setAttribute('disabled', true);
    }
});

// 確認訂購並付款
function confirmBooking(event) {
    event.preventDefault()
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('信用卡資訊填寫錯誤，請檢查後再試一次');
        return;
    };
    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('付款失敗，請確認信用卡資訊後再試一次');
            console.log(result.status);
            return;
        };
        let token = localStorage.getItem('token');
        let prime = result.card.prime;
        let contactFormData = new FormData(document.querySelector('#contact_form'));
        let contactData = {
            'name': contactFormData.get('name'),
            'email': contactFormData.get('email'),
            'phone': contactFormData.get('phone'),
        };
        let orderData = {
            'prime': prime,
            'order': bookingData,
            'contact': contactData
        };
        let src = '/api/orders';
        let options = {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        };
        let alertErrorMsg = {
            '會員未登入': '請先登入會員',
            '無法連線到資料庫': '系統忙碌中，請稍後再試'
        }
        ajax(src, options).then((data) => {
            if(data.ok){
                // 成功付款，導向感謝頁面(?
            }else{
                alert(alertErrorMsg[data['message']]);
            }
        })
        // send prime to your server, to pay with Pay by Prime API .
        // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
    })
}
