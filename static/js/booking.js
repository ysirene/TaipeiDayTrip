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

// 確認訂購並付款
function confirmBooking(event){

};