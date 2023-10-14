const attraction_id = window.location.pathname.split('/')[2];
let totalImages = 0;

// 連線到該景點並取得資料
(function getAttractionInfo(){
    let src = `/api/attraction/${attraction_id}`;
    let options = {};
    ajax(src, options).then((data) => {
        if(data.error){
            if(data.message === 'cannot connect to database'){
                alert('系統忙碌中，請稍後再試')
            }
            window.location.href = '/';
        }else{
            document.getElementsByTagName('body')[0].style.display = 'block';
            let attractionNameElem = document.querySelector('.profile__info_name');
            let attractionCatMrtElem = document.querySelector('.profile__info_cat_mrt');
            let attractionDescriptionElem = document.querySelector('#description');
            let attractionAddressElem = document.querySelector('#address');
            let attractionTransportElem = document.querySelector('#transport');
            attractionNameElem.textContent = data['data']['name'];
            attractionCatMrtElem.textContent = data['data']['category'] + ' at ' + data['data']['mrt'];
            attractionDescriptionElem.textContent = data['data']['description'];
            attractionAddressElem.textContent = data['data']['address'];
            attractionTransportElem.textContent = data['data']['transport'];
            // 處理照片輪播
            let imagesArr = data['data']['images'];
            let slideContainerElem = document.querySelector('.profile__slide_show');
            totalImages = imagesArr.length;
            for(let i=0;i<imagesArr.length;i++){
                let image = document.createElement('img');
                image.setAttribute('src', imagesArr[i]);
                if(i==0){
                    image.className = 'fade_in';
                }else{
                    image.className = 'hide_img';
                };
                slideContainerElem.appendChild(image);
            };
            for(let i=0;i<imagesArr.length;i++){
                let slideChoiceElem = document.querySelector('.profile__slide_choice');
                let choiceSpan = document.createElement('span')
                choiceSpan.setAttribute('onclick',`changeSlide(${i})`);
                if(i == 0){
                    choiceSpan.style.backgroundImage = 'url(../static/image/img_picker_b.png)';
                    choiceSpan.id = 'choice_picked';
                };
                slideChoiceElem.appendChild(choiceSpan);
            };
        };
    });
})();
let currentSlideIdx = 0;
function changeSlide(num){
    let fadeOutSlide = document.querySelector('.fade_in');
    let pastChoiceElem = document.querySelector('#choice_picked');
    let choiceElem = document.querySelector('.profile__slide_choice').children[num];
    let imgElem = document.getElementsByTagName('img');
    fadeOutSlide.className = 'fade_out';
    imgElem[num].className = 'fade_in';
    pastChoiceElem.style.backgroundImage = 'url(../static/image/img_picker_w.png)';
    pastChoiceElem.removeAttribute('id');
    choiceElem.style.backgroundImage = 'url(../static/image/img_picker_b.png)';
    choiceElem.id = 'choice_picked';
}
function prevSlide(){
    currentSlideIdx = (currentSlideIdx - 1 + totalImages) % totalImages;
    changeSlide(currentSlideIdx);
};
function nextSlide(){
    currentSlideIdx = (currentSlideIdx + 1) % totalImages;
    changeSlide(currentSlideIdx);
};
// 最早的預約日期是今天
let today = new Date().toISOString().split('T')[0];
let bookingDateElem = document.querySelector('.booking__date');
bookingDateElem.min = today;
// 根據時段改變價錢
let bookingTimeElem = document.querySelectorAll('input[name="time"]');
let bookingPriceElem = document.querySelector('.booking__price');
bookingTimeElem.forEach((elem) => {
    elem.addEventListener('change', function(event){
        time = event.target.value;
        if(time == 'forenoon'){
            bookingPriceElem.textContent = '新台幣 2000 元';
        }else{
            bookingPriceElem.textContent = '新台幣 2500 元';
        };
    });
});
// 將預定行程加入購物車
function addItemToCart(event){
    event.preventDefault();
    if(signinStatus === false){
        toggleSigninSignup();
    }
    else{
        let bookingFormData = new FormData(document.querySelector('#booking_form'));
        let price = bookingFormData.get('time') === 'forenoon'? 2000: 2500;
        let bookingData = {
            'attractionId': attraction_id,
            'date': bookingFormData.get('date'),
            'time': bookingFormData.get('time'),
            'price': price
        };
        let token = localStorage.getItem('token');
        let src = '/api/booking';
        let options = {
            method: 'POST',
            headers: {
                'authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(bookingData)
        };
        let alertErrorMsg = {
            'not logged in': '請先登入會員',
            'cannot connect to database': '系統忙碌中，請稍後再試',
            'incorrect input': '預訂行程的資料有誤，請檢查後再提交一次'
        };
        ajax(src, options).then((data) => {
            if(data.ok){
                window.location.href = '/booking';
            }else{
                alert(alertErrorMsg[data.message]);
            };
        });
    };
};