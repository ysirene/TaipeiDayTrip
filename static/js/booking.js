let bookingData = {};

// 查無訂單或連線錯誤時顯示訊息
function renderBookingNotification(msg, type){
    let messageTypeColors = {
        'emptyCart': '#666',
        'error': '#ab4d4d'
    }
    let bookingInfoElem = document.querySelector('#booking_info--none');
    let textElem = document.querySelector('.none__text');
    textElem.textContent = msg;
    textElem.style.color = messageTypeColors[type];
    bookingInfoElem.className= '';
};
// 渲染會員個人資訊
function renderMemberInfo(data){
    let bodyElem = document.getElementsByTagName('body')[0];
    let memberNameElem = document.querySelectorAll('#member_name');
    let memberEmailElem = document.querySelector('#member_email');
    memberNameElem[0].textContent = data.data.name;
    memberNameElem[1].value = data.data.name;
    memberEmailElem.value = data.data.email;
    bodyElem.style.display = 'block';
};
// 渲染預定行程資訊
function renderBookingInfo(data){
    let bookingInfoElem = document.querySelector('#booking_info');
    let attractionNameElem = document.querySelector('#attraction_name');
    let attractionAddressElem = document.querySelector('#attraction_address');
    let attractionImgElem =  document.querySelector('#attraction_img');
    let bookingDateElem = document.querySelector('#booking_date');
    let bookingTimeElem = document.querySelector('#booking_time');
    let bookingPriceElem = document.querySelector('#booking_price');
    let amountElem = document.querySelector('#amount');
    let bookingDate = new Date(data.data.date);
    let formattedDate = formatDate(bookingDate);
    let bookingTime = data.data.time == 'forenoon'? '早上9點到中午12點': '下午1點到4點';
    bookingInfoElem.className= '';
    attractionNameElem.textContent = data.data.attraction.name;
    attractionAddressElem.textContent = data.data.attraction.address;
    attractionImgElem.setAttribute('src', data.data.attraction.image);
    bookingDateElem.textContent = formattedDate;
    bookingTimeElem.textContent = bookingTime;
    bookingPriceElem.textContent = data.data.price;
    amountElem.textContent = data.data.price;
};
// 驗證會員並渲染會員資訊與訂單
function authenticateUserAndShowBookingInfo(){
    let memberBtnElem = document.querySelector('#member_btn');
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
            if(data.data != null){
                memberBtnElem.textContent = '登出系統';
                memberBtnElem.setAttribute('onclick', 'signout()');
                memberBtnElem.classList.remove('elem--invisible');
                signinStatus = true
                renderMemberInfo(data);
                getBookingInfo();
            }else if(data.data == null){
                window.location.href = '/';
            };
        }).catch((error) => {
            console.log(error);
        });
    }else{
        window.location.href = '/';
    };
};
authenticateUserAndShowBookingInfo()

// 將預定行程資料中的日期格式化
function formatDate(date){
    let year = date.getFullYear();
    let month = (date.getMonth() + 1).toString().padStart(2, '0');
    let day = date.getDate().toString().padStart(2, '0');
    let formattedDate = `${year}-${month}-${day}`;
    return formattedDate
};

// 更新預定行程資訊 for下訂單時用
function setBookingData(data){
    let bookingDate = new Date(data.data.date);
    let formattedDate = formatDate(bookingDate);
    bookingData = {
        'price': data.data.price,
        'trip': {
            'attraction': data.data.attraction,
            'date': formattedDate,
            'time': data.data.time
        }
    };
};

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
        if(data.error && data.message == 'not logged in'){
            window.location.href = '/'; 
        }else if(data.error && data.message == 'cannot connect to database'){
            renderBookingNotification('系統忙碌中，暫時無法取得訂單資訊，請將網頁重新整理', 'error');
        }else if(data.data === null){
            renderBookingNotification('目前沒有任何待預訂的行程', 'emptyCart');
        }else{
            renderBookingInfo(data);
            setBookingData(data);
        };
    }).catch((error) => {
        console.log(error);
    });
};

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

function changeSubmitBtnToLoadingType(){
    let submitBtn = document.querySelector('.form__submit');
    let loadingBtn = document.querySelector('.form__submit--loading');
    submitBtn.classList.replace('elem--block', 'elem--hide');
    loadingBtn.classList.replace('elem--hide', 'elem--block');
};

function changeSubmitBtnToDefaultType(){
    let submitBtn = document.querySelector('.form__submit');
    let loadingBtn = document.querySelector('.form__submit--loading');
    submitBtn.classList.replace('elem--hide', 'elem--block');
    loadingBtn.classList.replace('elem--block', 'elem--hide');
}

// 確認訂購並付款
function confirmBooking(event) {
    event.preventDefault();
    changeSubmitBtnToLoadingType();
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert('信用卡資訊填寫錯誤，請檢查後再試一次');
        changeSubmitBtnToDefaultType();
        return;
    };
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('付款失敗，請確認信用卡資訊後再試一次');
            changeSubmitBtnToDefaultType();
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
            'not logged in': '請先登入會員',
            'cannot connect to database': '系統忙碌中，請稍後再試',
            'incorrect order information': '訂單資訊有誤，請檢查後再試',
            'incorrect contact information': '聯絡資訊填寫錯誤，請檢查後再試'
        };
        ajax(src, options).then((data) => {
            if(data.error){
                alert(alertErrorMsg[data.message]);
                changeSubmitBtnToDefaultType();
            }else{
                if(data.data.payment.status === 0){
                    let orderNumber = data.data.number;
                    window.location.href = `/thankyou?number=${orderNumber}`;
                }else{
                    alert('訂單編號 ' + data.data.number + ' 付款失敗。錯誤代碼：' + data.data.payment.status);
                    changeSubmitBtnToDefaultType();
                };
            };
        });
    });
};
