let nextPage = 0;
let keyword = '';
let attractionsElem = document.querySelector('.attractions');
let searchBtnElem = document.querySelector('.search_bar__button');
let searchKeywordElem = document.querySelector('.search_bar__box');
let leftArrowElem = document.querySelector('.list_bar__left_arrow');
let rightArrowElem = document.querySelector('.list_bar__right_arrow');
let containerElem = document.querySelector('.container');

// 驗證登入狀態
authenticateUser();

// 捲動顯示下一頁
const callback = (entries) => {
    if(entries[0].isIntersecting && nextPage != null){
        getAttractionsData(nextPage, keyword);
        observer.unobserve(entries[0].target);
    }else if(nextPage == null){
        observer.disconnect();
    };
};
const observer = new IntersectionObserver(callback);
// 捷運清單捲動
leftArrowElem.addEventListener('click', () => {
    containerElem.scrollLeft -= (containerElem.clientWidth-100);
});
rightArrowElem.addEventListener('click', () => {
    containerElem.scrollLeft += (containerElem.clientWidth-100);
});
// 捷運站清單按鈕
function searchMrt(btn){
    searchKeywordElem.value = btn.textContent;
    searchBtnElem.click();
};
// 取得捷運列表
(function getMrtsList(){
    let src = '/api/mrts';
    let options = {};
    ajax(src, options).then((data) => {
        for(let i=0; i<data['data'].length; i++){
            if (data['data'][i] != 'None'){
                let mrtButton = document.createElement('button');
                mrtButton.className = 'list_item';
                mrtButton.setAttribute('onclick', 'searchMrt(this)');
                mrtButton.textContent = data['data'][i];
                containerElem.appendChild(mrtButton);
            };
        };
    }).catch((error) => {
        console.log(error);
    });
})();
// 將取得的data渲染到畫面
function renderAttractions(data){
    for(i=0; i<data['data'].length; i++){
        let attractionBoxDiv = document.createElement('div');
        attractionBoxDiv.className = 'attraction__box';
        let attractionImg = document.createElement('img');
        attractionImg.setAttribute('src',data['data'][i]['images'][0]);
        let attractionNameDiv = document.createElement('div');
        attractionNameDiv.className = 'attraction__name';
        attractionNameDiv.textContent = data['data'][i]['name'];
        let attractionDetailDiv = document.createElement('div');
        attractionDetailDiv.className = 'attraction__detail';
        let mrtDiv = document.createElement('div');
        mrtDiv.textContent = data['data'][i]['mrt'];
        let catDiv = document.createElement('div');
        catDiv.textContent = data['data'][i]['category'];
        let url = document.createElement('a');
        url.setAttribute('href', `/attraction/${data['data'][i]['id']}`);
        attractionDetailDiv.appendChild(mrtDiv);
        attractionDetailDiv.appendChild(catDiv);
        attractionBoxDiv.appendChild(attractionImg);
        attractionBoxDiv.appendChild(attractionNameDiv);
        attractionBoxDiv.appendChild(attractionDetailDiv);
        url.appendChild(attractionBoxDiv);
        attractionsElem.appendChild(url);
    };
};
// 無法取得景點資料時，顯示錯誤訊息
function renderAttractionsDataError(errorMsg){
    let mainElem = document.querySelector('main');
    let errorMessageDiv = document.createElement('div');
    errorMessageDiv.className = 'attraction__error_msg';
    errorMessageDiv.textContent = errorMsg;
    mainElem.appendChild(errorMessageDiv);
}
// 取得景點DATA後渲染&無限捲動
function getAttractionsData(page, keyword){
    let src = `/api/attractions?page=${encodeURIComponent(page)}&keyword=${encodeURIComponent(keyword)}`;
    let options = {};
    ajax(src, options).then((data) => {
        if(data.message === 'cannot connect to database'){
            renderAttractionsDataError('連線失敗，若欲查看更多景點請重新整理網頁');
        };
        nextPage = data['nextPage'];
        if(data.data.length === 0){
            renderAttractionsDataError('沒有相關的景點');
        }else{
            renderAttractions(data);
            observer.observe(document.querySelector('.attractions').lastChild);
        }
    }).catch((error) => {
        console.log(error);
    });
};
// 搜尋框按鈕
searchBtnElem.addEventListener('click', function(e){
    e.preventDefault();
    let attractionsDataErrorMsgElem = document.querySelector('.attraction__error_msg');
    keyword = searchKeywordElem.value;
    nextPage = 0;
    while (attractionsElem.hasChildNodes()){
        attractionsElem.removeChild(attractionsElem.lastChild);
    };
    if(attractionsDataErrorMsgElem){
        attractionsDataErrorMsgElem.remove();
    }
    getAttractionsData(nextPage, keyword);
});
getAttractionsData(nextPage, keyword);